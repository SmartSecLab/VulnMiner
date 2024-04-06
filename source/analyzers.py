# -*- coding: utf-8 -*-
"""
Copyright (C) 2023 SmartSecLab,
Kristiania University College- All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: https://opensource.org/licenses/MIT
@Programmer: Guru Bhandari

Grepping functions from the vulnerability context of the file.
Fetching the functions which have given line context/statement.
"""
import time
import os
import json
import subprocess as sub
import xml.etree.ElementTree as et
from io import StringIO
from pathlib import Path
from threading import Timer
from tabulate import tabulate
import numpy as np
import pandas as pd
from source.utility import Utility


class Analyzers:
    """This class applies static code analyzers via commands
    """

    def __init__(self, config: dict):
        self.common_cols = ["file", "line", "column", "cwe", "note"]
        self.unique_cols = ["context", "defaultlevel", "level", "helpuri"]
        self.filter_cols = [
            "toolversion",
            "fingerprint",
            "ruleid",
            "suggestion",
        ]
        self.consider_cols = ['file', 'line', 'column', 'defaultlevel',
                              'level', 'category', 'name', 'msg', 'note',
                              'cwe', 'context', 'helpuri', 'severity',
                              'tool', 'type'
                              ]
        self.pl_list = ["c", "c++", "cpp", "cxx",
                        "cp", "cc", "h", "hpp", "hxx", "hh"]

        self.util = Utility()
        self.config = config

    def guess_pl(self, file, zip_obj=None) -> str:
        """guess the programming language of the input file.
        Recursively Remove .DS_Store which was introducing encoding error,
        https://jonbellah.com/articles/recursively-remove-ds-store
        ignore all files with . start and compiled sources
        """
        pl = 'unknown'

        if self.config['save']["apply_guesslang"]:
            from guesslang import Guess
            guess = Guess()
            try:
                if zip_obj is not None:
                    # extract a specific file from the zip container
                    with zip_obj.open(file, "r") as fp:
                        lang = guess.language_name(fp.read())
                else:
                    with open(file, "r") as fp:
                        lang = guess.language_name(fp.read())
                pl = lang.lower()
            except Exception as exc:
                print(f"Guesslang error: {exc}")

        else:
            pl = Path(file).suffix.replace(".", "").lower()
            pl = pl if pl in self.pl_list else "unknown"

        return pl

    ##################### Applying CppCheck tool ##################

    def get_statement(self, file, line):
        statement = ""
        try:
            with open(file, encoding='latin-1') as fp:
                lines = fp.readlines()
                if line < len(lines):
                    statement = lines[line]
        except Exception as exc:
            print(f"Encoding Error at CppCheck: {exc}")
        return statement

    def fetch_location(self, flaw: et.Element) -> dict:
        """get locations of all the error list generated by CppCheck"""
        dt_loc = {"line": [], "column": [], "info": []}

        for loc in flaw.findall("location"):
            if 'line' in loc.attrib.keys():
                dt_loc['line'].append(loc.attrib['line'])
            if 'column' in loc.attrib.keys():
                dt_loc['column'].append(loc.attrib['column'])
            if 'info' in loc.attrib.keys():
                dt_loc['info'].append(loc.attrib['info'])
        return dt_loc

    def correct_label(self, df):
        if len(df):
            # explode the line row on each list of items
            df = df.explode("line")
            df["line"] = df.line.astype(dtype=int, errors="ignore")
            df["tool"] = "CppCheck"

            # To make CWE column values uniform to FlawFinder output
            df["cwe"] = (
                "CWE-" + df["cwe"]
                if set(["cwe"]).issubset(df.columns)
                else "CWE-unknown"
            )
            df = df.reset_index(drop=True)
            return df
        else:
            return pd.DataFrame()

    def xml2df_cppcheck(self, xml: str) -> pd.DataFrame:
        """convert xml str of cppcheck to dataframe"""
        df = pd.DataFrame()
        xtree = et.fromstring(xml)
        for errors in xtree.findall(".//errors"):
            for err in errors.findall("error"):
                dt_err = err.attrib
                # get the location of the vulnerable line content
                dt_err.update(self.fetch_location(err))
                df = pd.concat(
                    [df, pd.DataFrame([dt_err])],
                    ignore_index=True)
        if len(df):
            # df = df.rename(columns={"file0": "file"}
            #                ).reset_index(drop=True)
            df = df.drop(columns=["file0"], axis=1,
                         errors="ignore").reset_index(drop=True)
        return df

    def apply_cppcheck(self, file: str) -> pd.DataFrame:
        """find flaws in the file using CppCheck tool
        """
        df = pd.DataFrame()
        cmd = "cppcheck -f " + file + " --xml --xml-version=2"
        # avoid shell=True, it works but doesn't stop at Timeout
        process = sub.Popen(cmd.split(), stdout=sub.PIPE, stderr=sub.STDOUT)
        timer = Timer(2, process.kill)
        try:
            timer.start()
            stdout, stderr = process.communicate()
            df = self.xml2df_cppcheck(xml=stdout.decode("utf-8"))
            df = self.correct_label(df)
            # adding context since cppcheck does not report statement,
            # index starts from zero, therefore row.line-1
            df['context'] = ''
            df['context'] = df.apply(
                lambda row: self.get_statement(file, row.line-1), axis=1)
            df['file'] = file
        except Exception as exc:
            print(f"CppCheck error: {exc}")
        finally:
            timer.cancel()
        return df

######################### Applying FlawFinder tool ####################

    def apply_flawfinder(self, fname: str) -> pd.DataFrame:
        """find flaws in the file using CppCheck tool"""
        cmd = ''
        df = pd.DataFrame()
        try:
            if os.path.isfile(fname):
                cmd = "flawfinder --csv " + fname
            elif os.path.isdir(fname):
                cmd = "flawfinder --csv --inputs " + fname
            else:
                print("Please provide a valid project dir/file/link!")

            process = sub.Popen(
                cmd,
                shell=True,
                stdout=sub.PIPE,
            )
            output = process.stdout.read().decode("utf-8")
            df = pd.read_csv(StringIO(output))

            if len(df) > 0:
                df["tool"] = "FlawFinder"
            df = df.reset_index(drop=True)
        except Exception as err:
            print(f'Error parsing file using flawfinder: {err}\nFile:{fname}')
        return df

######################## Applying Rats tool #########################

    @staticmethod
    def xml2df_rats(xml) -> pd.DataFrame:
        """convert xml file of rats tool to dataframe"""
        df = pd.DataFrame()
        if isinstance(xml, str):
            xtree = et.fromstring(xml)

            for err in xtree.findall("vulnerability"):
                dt = {
                    "severity": err.find("severity").text,
                    "type": err.find("type").text if err.find("type") is not None else None,
                    "message": err.find("message").text,
                }
                for loc in err.findall("file"):
                    dt["file"] = loc.find("name").text

                    for line in loc.findall("line"):
                        dt["line"] = line.text
                        df = pd.concat([df, pd.DataFrame([dt])],
                                       ignore_index=True)
            if len(df):
                df = df.reset_index(drop=True)
        return df

    def apply_rats(self, fname: str) -> pd.DataFrame:
        """ The Rough Auditing Tool for Security is an open-source tool
        developed by Secure Software Engineers
        https://security.web.cern.ch/recommendations/en/codetools/rats.shtml \
        For example:
        `rats --quiet --xml -w 3 data/projects/contiki-2.4/apps/`
        """
        # rats --quiet --xml -w 3 <dir_or_file>
        cmd = ["rats --quiet --xml -w 3 " + fname]
        output = None
        try:
            process = sub.Popen(
                cmd, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
            # output = process.stdout.read().decode("utf-8")
            # err = process.stderr.read().decode("utf-8")
            output, err = process.communicate()
            if output:
                output = output.decode("utf-8")
            if err:
                print(
                    f"Error at Rats while parsing: {err.decode('utf-8')} on file: {fname}")
                output = None

        except Exception as exc:
            print(f"Error at Rats: {exc} on file: {fname}")

        df = self.xml2df_rats(output)

        if len(df):
            # RATS tool does not produce results with CWE type.
            df["cwe"] = "CWE-unknown"
            df["line"] = df.line.astype(int)
            df["tool"] = "Rats"
            df = df.reset_index(drop=True)
            # print(tabulate(df, headers='keys', tablefmt='pretty'))
        return df


########################### Applying infer tool ##########################


    def json2df(self, file: str) -> pd.DataFrame:
        df = pd.DataFrame()
        try:
            with open(file) as f:
                data = json.load(f)
            df = pd.DataFrame(data)
        except Exception as exc:
            print(f"json2df error [{exc}]: opening at: {file}")
        return df

    def apply_infer(self, fname: str) -> pd.DataFrame:
        """TODO: find flaws in the file using infer tool"""
        infer_dir = 'infer-output'

        if os.path.isfile(fname):
            cmd = "infer run --results-dir " + infer_dir + " -- gcc -c " + fname
        elif os.path.isdir(fname):
            print('Please provide a valid file, not a path for infer tool!')
        else:
            print("Please provide a valid project dir/file/link!")

        process = sub.Popen(
            cmd,
            shell=True,
            stdout=sub.PIPE,
        )
        process.wait()
        file = infer_dir + '/report.json'
        df = self.json2df(file)

        if len(df) > 0:
            df["tool"] = "infer"
            df = df.reset_index(drop=True)
        return df


########## Prerequisites for merging the output of all tools ###########


    @ staticmethod
    def concat(*args):
        """merge two columns of the dataframe with numpy vectorize method"""
        concat_str = ""
        try:
            strs = [str(arg) for arg in args if not pd.isnull(arg)]
            concat_str = ",".join(strs) if strs else np.nan
        except Exception as exc:
            print("Value Error: ", exc)
            print(f"Args: {args}")
            print(concat_str)
        return concat_str

    def adjust_cols(self, df_ff, df_cc, df_rat):
        # Adjusting columns generated by FlawFinder, CppCheck and Rats tool
        df_ff = df_ff.rename(columns=str.lower, errors="ignore")
        df_ff = df_ff.rename(
            columns={"cwes": "cwe", "warning": "msg"},
            errors="ignore")
        df_cc = df_cc.rename(
            columns={"info": "note", "id": "name"},
            errors="ignore")
        df_rat = df_rat.rename(
            columns={"message": "msg", "type": "category"},
            errors="ignore")

        # CppCheck: 'msg' and 'verbose' columns with same entries,
        # so let's keep only 'msg'.
        df_cc = (df_cc.drop(
            columns=["verbose"],
            axis=1,
            errors="ignore"))
        # do this after merging 'suggestion to 'note' column
        if len(df_ff) > 0:
            df_ff["note"] = (
                df_ff["suggestion"].astype(
                    str) + "  " + df_ff["note"].astype(str)
            )
            df_ff = df_ff.drop(
                columns=["suggestion", "note"],
                axis=1,
                errors="ignore")
        return df_ff, df_cc, df_rat


######################## Merge the output of all tools #################

    def merge_tools_result(self, fname) -> pd.DataFrame:
        """merge dataframe generated by FlawFinder and CppCheck tools"""
        # apply tools:
        # print('Applying flawfinder...')
        df_ff = self.apply_flawfinder(fname=fname)
        # print('Applying cppcheck...')
        df_cc = self.apply_cppcheck(file=fname)
        # print('Applying rats...')
        df_rat = self.apply_rats(fname=fname)
        # df_infer = self.apply_infer(fname=fname)

        df_merged = pd.DataFrame()

        if len(df_ff) > 0 or len(df_cc) > 0 or len(df_rat) > 0:
            df_ff, df_cc, df_rat = self.adjust_cols(df_ff, df_cc, df_rat)
            df_merged = pd.concat([df_ff, df_cc, df_rat]
                                  ).reset_index(drop=True)
            df_merged = df_merged.drop(columns=self.filter_cols,
                                       axis=1, errors="ignore")
            # print(f"columns of merged dataframe: \n{df_merged.columns}")

            # =================================ADD===============================
            # ADD severity column if not present in the merged dataframe.
            if 'severity' not in list(df_merged.columns):
                df_merged['severity'] = '-'
            if 'category' not in list(df_merged.columns):
                df_merged['category'] = '-'
            if 'msg' not in list(df_merged.columns):
                df_merged['msg'] = '-'
            if 'column' not in list(df_merged.columns):
                df_merged['column'] = '-'
            if 'helpuri' not in list(df_merged.columns):
                df_merged['helpuri'] = '-'
            if 'defaultlevel' not in list(df_merged.columns):
                df_merged['defaultlevel'] = '-'
            if 'level' not in list(df_merged.columns):
                df_merged['level'] = '-'
            if 'note' not in list(df_merged.columns):
                df_merged['note'] = '-'
            if 'name' not in list(df_merged.columns):
                df_merged['name'] = '-'
            if 'type' not in list(df_merged.columns):
                df_merged['type'] = '-'

            if 'context' not in list(df_merged.columns):
                df_merged['context'] = '-'

            # ===============REMOVE===================
            # REMOVE columns if present in the merged dataframe.
            # if table statement has column named inconclusive
            if 'inconclusive' in list(df_merged.columns):
                df_merged = df_merged.drop(
                    columns=['inconclusive'], axis=1, errors="ignore")

            # =============FILTER NAN===================
            # Necessary columns
            df_merged = df_merged[df_merged["line"].notna()]
            df_merged = df_merged[df_merged["cwe"].notna()]

            # '-' for empty cells
            df_merged = df_merged.fillna("-")
            df_merged['context'] = df_merged.context.astype(str).str.strip()
            df_merged = df_merged[self.consider_cols]
            df_merged['file'] = fname
        return df_merged
