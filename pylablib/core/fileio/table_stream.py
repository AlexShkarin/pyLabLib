from ..utils import string, files as file_utils

import time
import os


class TableStreamFile:
    """
    Expanding table file.

    Can define column names and formats for different columns, and repeatedly write data into the same file.
    Useful for, e.g., continuous log files.
    
    Args:
        path (str): Path to the destination file.
        columns (list): If not ``None``, it's a list of column names to be added as a header on creation.
        delimiter (str): Values delimiter.
        fmt (str): If not ``None``, it's a list of format strings for the line entries (e.g., ``".3f"``);
            instead of format string one can also be ``None``, which means using the standard :func:`.to_string` conversion function
        add_timestamp (bool): If ``True``, add the UNIX timestamp in the beginning of each line (columns and format are expanded accordingly)
        header_prepend: the string to prepend to the header line; by default, a comment symbol, which is best compatibly with :func:`.loadfile.load_csv` function
    """
    def __init__(self, path, columns=None, delimiter="\t", fmt=None, add_timestamp=False, header_prepend="# "):
        self.path=path
        self.delimiter=delimiter
        self.columns=columns
        self.add_timestamp=add_timestamp
        self.fmt=fmt
        self.header_prepend=header_prepend
        
    def _get_path(self, line, timestamp):  # pylint: disable=unused-argument
        """
        Generate file path based on the data line and timestamp.

        Can be overloaded in subclasses to implement various naming schemes (e.g., generate new file name every day).
        Data line can be a string (when called from :meth:`write_text_lines`) or a row of values
        (when called from :meth:`write_row` or :meth:`write_multiple_rows`). If multiple lines are written, only the first one is passed.
        """
        return self.path
    def _get_timestamp(self, timestamp):
        return "{:.3f}".format(timestamp)
    def _get_header(self):
        """
        Generate header string.

        Can be overloaded in subclasses to implement more descriptive headers.
        """
        if self.columns:
            columns=self.columns
            if self.add_timestamp:
                columns=["Timestamp"]+columns
            return self.header_prepend+self.delimiter.join(columns)+"\n"
        else:
            return None

    def _write_lines(self, lines, timestamp=None):
        path=self._get_path(lines[0],timestamp)
        if os.path.exists(path):
            with open(path,"a") as f:
                f.write("\n"+"\n".join(lines))
        else:
            file_utils.ensure_dir(os.path.split(path)[0])
            with open(path,"a") as f:
                header=self._get_header()
                if header:
                    f.write(header)
                f.write("\n"+"\n".join(lines))
                
    def write_text_lines(self, lines):
        """
        Write several text lines into the file.
        
        Create the file if it doesn't exist (in which case the header is automatically added).
        
        Args:
            lines ([str]): List of lines to write.
        """
        if not lines:
            return
        self._write_lines(lines)
    def write_row(self, row):
        """
        Write a single data row into the file. 
        
        Create the file if it doesn't exist (in which case the header is automatically added).
        
        Args:
            data (list or numpy.ndarray): Data row to be added.
        """
        self.write_multiple_rows([row])
    def write_multiple_rows(self, rows):
        """
        Write a multiple data lines into the file.
        
        Create the file if it doesn't exist (in which case the header is automatically added).
        
        Args:
            rows ([list or numpy.ndarray]): Data rows to be added.
        """
        if len(rows)==0:
            return
        datalen=len(rows[0])
        if self.columns and len(self.columns)!=datalen:
            raise ValueError("length of data row {} doesn't agree with the number of columns {}".format(datalen,len(self.columns)))
        if self.fmt and len(self.fmt)!=datalen:
            raise ValueError("length of data row {} doesn't agree with the number of format strings {}".format(datalen,len(self.fmt)))
        if self.fmt is None:
            fmt=[None]*datalen
        else:
            fmt=[None if f is None else "{:"+f+"}" for f in self.fmt]
        lines=[]
        timestamp=time.time() if self.add_timestamp else None
        timestamp_str=self._get_timestamp(timestamp) if timestamp else None
        for r in rows:
            r=[string.to_string(v,location="entry") if f is None else f.format(v) for f,v in zip(fmt,r)]
            if timestamp:
                r=[timestamp_str]+r
            line=self.delimiter.join(r)
            lines.append(line)
        self._write_lines(lines,timestamp=timestamp)