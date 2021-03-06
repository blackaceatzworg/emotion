#!/usr/bin/python
# -*- coding: utf-8 -*-

#======================================================================#
# 
# Description: A script to parse the British Hansard files in the Political Mashup XML format.
# 						Will output speeches by quarter and save them in the output-directory. 
# 
# Usage: 
# python modern-hansard-parser.py [path-to-xml-file] [output-directory]
# 
# Author: K. Beelen
# 
#======================================================================#

from lxml import etree as Etree
from datetime import datetime as dt
import os, codecs,re

#---------------------------------------------------------------------------------------------------------------------------------------------------------------#

class XML_to_TSV(object):
    def __init__(self,min_date="",max_date="",inpath,outpath):
        self.directory = inpath
        self.min_date = date(min_date)
        self.max_date = date(max_date)
        self.output_data = codecs.open(outpath+'/UKHansard-%sto%s.tsv'%(min_date,max_date),"w",encoding="utf-8")
        self.namespaces = {"pm":"http://www.politicalmashup.nl"}        
        self.namespaces_mads = {"mads":"http://www.loc.gov/mads/v2"}
        self.gender_dict = {}
        
    def makeTable(self):
        years_all = [f for f in sorted(os.listdir(self.directory)) if f.startswith("uk")]
        for y in years_all:
                doc_date = date(y.split(".")[-2])
                if doc_date >= self.min_date and doc_date <= self.max_date:
                        print y
                        self.SpeechXMLtoTSV(os.path.join(self.directory,y))

    def SpeechXMLtoTSV(self,xml_file): 
        date = xml_file.split("/")[-1].split(".")[-2]
        with open(xml_file,'rt') as xmlf:
                tree = Etree.parse(xmlf)
                topics =self.getELementsbyXpath(""".//pm:topic""",tree)
                for topic in topics:
                        topic_title = self.getElementsAttrbyXpath("""@pm:title""",topic)
                        scenes = self.getELementsbyXpath("""pm:scene""",topic)
                        if len(scenes) > 0:
                                for scene in scenes:
                                        scene_title = self.getElementsAttrbyXpath("""@pm:title""",scene)
                                        self.getSpeeches(scene,topic_title,scene_title,date)
                        else:
                                scene_title = "NA"
                                self.getSpeeches(topic,topic_title,scene_title,date)
                        
    def getSpeeches(self,parent_element,topic_title,scene_title,date):
        speeches = self.getELementsbyXpath(""".//pm:speech""",parent_element)
        for speech in speeches:
                speech_id = self.getElementsAttrbyXpath("""@pm:id""",speech)
                speaker_ref = self.getElementsAttrbyXpath("""@pm:member-ref""",speech)
                speaker_party = self.getElementsAttrbyXpath("""@pm:party""",speech)
                speaker_role = self.getElementsAttrbyXpath("""@pm:role""",speech)
	        speaker_name = self.getElementsAttrbyXpath("""@pm:speaker""",speech)
                speaker_function = self.getElementsAttrbyXpath("""@pm:function""",speech)                        
                paragraphs = self.getELementsbyXpath(".//pm:p",speech)
                text = u" ".join([Etree.tostring(para,method="text",encoding="unicode") for para in paragraphs])
                text = re.compile(ur"[\t\n\r\u2026\u2029]",re.DOTALL).sub(" ",text)
                self.output_data.write(u"{}\n".format(text,))
    
    def getElementsAttrbyXpath(self,xpath,element):
        results = element.xpath(xpath,namespaces=self.namespaces)
        if len(results) > 0: return results[0]
        else: return "NA"
        
    def getELementsbyXpath(self,xpath,element):
        return element.xpath(xpath,namespaces=self.namespaces)

class Table:
        def __init__(self,tsvfile,min_date="",max_date="",topic_term="",scene_term="",speech_term=""):
                self.data = tsvfile
                self.min_date = date(min_date)
                self.max_date = date(max_date)
                self.topic_term = topic_term
                self.scene_term = scene_term
                self.speech_term = speech_term
                self.output = codecs.open(os.path.join("/".join(tsvfile.split("/")[:-1]),"reducedUKHansard-ymin{}-ymax{}-top{}-sc{}-sp{}.tsv".format(min_date,max_date,self.topic_term,self.scene_term,self.speech_term)),"w",encoding='utf-8')
                
        def getRows(self):
                self.output.write("SPEECH\n")
                with codecs.open(self.data,encoding="utf-8") as data_file:
                        for line in data_file:
                                try:
                                        l = rowData(line)
                                        if date(l.date) < self.min_date: continue
                                        if date(l.date) > self.max_date: break

                                        self.selectRow_by_Content(l)
                                except Exception as e:
                                        print e, line

        def selectRow_by_Content(self,rowObject):
                        if self.speech_term in rowObject.speech.lower() and (self.scene_term in rowObject.scene or self.topic_term in rowObject.topic):
                                self.output.write(u"{}".format(rowObject.data))
                                print rowObject.speech_id
        
        def selectRow_by_Metadata(self,rowObject):
                pass
        
class rowData:
        def __init__(self,line):
                cells = line.split("\t")
                self.data = line
                self.speech = cells[0]
                #self.date = self.date

def date(date=None):
    if date == "current":
        date = dt.date(dt.now())
        yyyy,mm,dd = date.year,date.month,date.day
    elif len(date.split("-")) == 3:
        yyyy,mm,dd = date.split("-")
    else:
        yyyy,mm,dd = date.split("-")[0],"01","01"
    return dt(int(yyyy),int(mm),int(dd))


if __name__ == '__main__':
    listoffiles = [("1936-02-24","1936-03-31"),
				("1936-04-01","1936-06-30"),
				("1936-07-01","1936-07-31"),
                ("1936-10-29","1936-12-18"),
                ("1937-01-19","1937-03-25"),
                ("1937-04-06","1937-06-30"),
                ("1937-07-01","1937-07-30"),
                ("1937-10-21","1937-12-23"),
                ("1938-02-01","1938-03-31"),
                ("1938-04-01","1938-06-30"),
                ("1938-07-01","1938-09-28"),
                ("1938-10-03","1938-12-22"),
                ("1939-01-31","1939-03-31"),
                ("1939-04-03","1939-06-30"),
                ("1939-07-03","1939-09-29"),
                ("1939-10-02","1939-12-14"),
                ("1940-01-16","1940-03-21"),
                ("1940-04-02","1940-06-27"),
                ("1940-07-02","1940-09-19"),
                ("1940-10-08","1940-11-20"),
                ("1941-01-21","1941-03-27"),
                ("1941-04-01","1941-06-26"),
                ("1941-07-01","1941-09-30"),
                ("1941-10-01","1941-12-19"),
                ("1942-01-08","1942-03-26"),
                ("1942-05-19","1942-06-30"),
                ("1942-07-01","1942-09-30"),
                ("1942-10-01","1942-12-17"),
                ("1943-01-19","1943-03-31"),
                ("1943-04-01","1943-06-30"),
                ("1943-07-01","1943-09-24"),
                ("1943-10-12","1943-12-17"),
                ("1944-01-18","1944-03-31"),
                ("1944-04-04","1944-06-30"),
                ("1944-07-04","1944-09-29"),
                ("1944-10-03","1944-12-21"),
                ("1945-01-16","1945-03-29"),
                ("1945-04-10","1945-06-15"),
                ("1945-08-01","1945-08-24"),
                ("1945-10-09","1945-12-20"),
                ("1946-02-11","1946-03-22"),
                ("1946-04-30","1946-06-07"),
                ("1946-07-08","1946-08-02"),
                ("1946-10-08","1946-11-29"),
                ("1947-01-21","1947-03-31"),
                ("1947-04-01","1947-06-30"),
                ("1947-07-01","1947-08-13"),
                ("1947-10-20","1947-12-19"),
                ("1948-01-20","1948-03-25"),
                ("1948-04-06","1948-06-30"),
                ("1948-07-01","1948-09-24"),
                ("1948-10-25","1948-12-17"),
                ("1949-01-18","1949-03-31"),
                ("1949-04-01","1949-06-30"),
                ("1949-07-01","1949-09-29"),
                ("1949-10-18","1949-12-16"),
                ("1950-03-01","1950-03-31"),
                ("1950-04-03","1950-06-30"),
                ("1950-07-03","1950-09-19"),
                ("1950-10-17","1950-12-15"),
                ("1951-01-23","1951-03-22"),
                ("1951-04-03","1951-06-29"),
                ("1951-07-02","1951-08-02"),
                ("1951-10-04","1951-12-07"),
                ("1952-01-29","1952-03-31"),
                ("1952-04-01","1952-06-30"),
                ("1952-07-01","1952-08-01"),
                ("1952-10-14","1952-12-19"),
                ("1953-01-20","1953-03-31"),
                ("1953-04-01","1953-06-30"),
                ("1953-07-01","1953-07-31"),
                ("1953-10-20","1953-12-18"),
                ("1954-01-19","1954-03-11"),
                ("1954-04-05","1954-06-30"),
                ("1954-07-01","1954-07-30"),
                ("1954-10-19","1954-12-22"),
                ("1955-01-25","1955-03-31"),
                ("1955-04-01","1955-06-24"),
                ("1955-07-18","1955-07-28"),
                ("1955-10-25","1955-12-21"),
                ("1956-01-24","1956-03-29"),
                ("1956-04-10","1956-06-29"),
                ("1956-07-02","1956-09-14"),
                ("1956-10-23","1956-12-21"),
                ("1957-01-22","1957-03-29"),
                ("1957-04-01","1957-06-28"),
                ("1957-07-01","1957-08-02"),
                ("1957-10-29","1957-12-20"),
                ("1958-01-21","1958-03-31"),
                ("1958-04-01","1958-06-20"),
                ("1958-07-07","1958-08-01"),
                ("1958-10-23","1958-12-18"),
                ("1959-01-20","1959-03-26"),
                ("1959-04-07","1959-06-30"),
                ("1959-07-01","1959-09-18"),
                ("1959-10-20","1959-12-17"),
                ("1960-01-26","1960-03-31"),
                ("1960-04-01","1960-06-30"),
                ("1960-07-01","1960-07-29"),
                ("1960-10-25","1960-12-21"),
                ("1961-01-24","1961-03-30"),
                ("1961-04-11","1961-06-30"),
                ("1961-07-03","1961-08-04"),
                ("1961-10-17","1961-12-21"),
                ("1962-01-23","1962-03-30"),
                ("1962-04-02","1962-06-29"),
                ("1962-07-02","1962-08-03"),
                ("1962-10-25","1962-12-21"),
                ("1963-01-22","1963-03-29"),
                ("1963-04-01","1963-06-28"),
                ("1963-07-01","1963-08-02"),
                ("1963-10-24","1963-12-20"),
                ("1964-01-14","1964-03-26"),
                ("1964-04-07","1964-06-30"),
                ("1964-07-01","1964-07-31"),
                ("1964-10-27","1964-12-23"),
                ("1965-01-19","1965-03-31"),
                ("1965-04-01","1965-06-30"),
                ("1965-07-01","1965-08-05"),
                ("1965-10-26","1965-12-22"),
                ("1966-01-25","1966-03-10"),
                ("1966-04-18","1966-06-30"),
                ("1966-07-01","1966-08-12"),
                ("1966-10-18","1966-12-21"),
                ("1967-01-17","1967-03-23"),
                ("1967-04-04","1967-06-30"),
                ("1967-07-03","1967-07-28"),
                ("1967-10-23","1967-12-21"),
                ("1968-01-16","1968-03-29"),
                ("1968-04-01","1968-06-28"),
                ("1968-07-01","1968-08-27"),
                ("1968-10-14","1968-12-20"),
                ("1969-01-20","1969-03-31"),
                ("1969-04-01","1969-06-30"),
                ("1969-07-01","1969-07-25"),
                ("1969-10-13","1969-12-19"),
                ("1970-01-19","1970-03-26"),
                ("1970-04-06","1970-06-30"),
                ("1970-07-01","1970-07-24"),
                ("1970-10-27","1970-12-18"),
                ("1971-01-12","1971-03-31"),
                ("1971-04-01","1971-06-30"),
                ("1971-07-01","1971-09-23"),
                ("1971-10-18","1971-12-22"),
                ("1972-01-17","1972-03-29"),
                ("1972-04-10","1972-06-30"),
                ("1972-07-03","1972-08-09"),
                ("1972-10-17","1972-12-22"),
                ("1973-01-22","1973-03-30"),
                ("1973-04-02","1973-06-29"),
                ("1973-07-02","1973-07-25"),
                ("1973-10-16","1973-12-21"),
                ("1974-01-09","1974-03-29"),
                ("1974-04-01","1974-06-28"),
                ("1974-07-01","1974-07-31"),
                ("1974-10-22","1974-12-20"),
                ("1975-01-13","1975-03-27"),
                ("1975-04-07","1975-06-30"),
                ("1975-07-01","1975-08-07"),
                ("1975-10-13","1975-12-19"),
                ("1976-01-12","1976-03-31"),
                ("1976-04-01","1976-06-30"),
                ("1976-07-01","1976-08-06"),
                ("1976-10-11","1976-12-23"),
                ("1977-01-10","1977-03-31"),
                ("1977-04-01","1977-06-30"),
                ("1977-07-01","1977-07-28"),
                ("1977-10-26","1977-12-16"),
                ("1978-01-09","1978-03-23"),
                ("1978-04-03","1978-06-30"),
                ("1978-07-03","1978-08-03"),
                ("1978-10-24","1978-12-15"),
                ("1979-01-15","1979-03-30"),
                ("1979-04-02","1979-06-29"),
                ("1979-07-02","1979-07-27"),
                ("1979-10-22","1979-12-21"),
                ("1980-01-14","1980-03-31"),
                ("1980-04-01","1980-06-30"),
                ("1980-07-01","1980-08-08"),
                ("1980-10-27","1980-12-19"),
                ("1981-01-12","1981-03-31"),
                ("1981-04-01","1981-06-30"),
                ("1981-07-01","1981-07-31"),
                ("1981-10-19","1981-12-23"),
                ("1982-01-18","1982-03-31"),
                ("1982-04-01","1982-06-30"),
                ("1982-07-01","1982-07-30"),
                ("1982-10-18","1982-12-23"),
                ("1983-01-17","1983-03-31"),
                ("1983-04-11","1983-06-30"),
                ("1983-07-01","1983-07-29"),
                ("1983-10-24","1983-12-22"),
                ("1984-01-16","1984-03-30"),
                ("1984-04-02","1984-06-29"),
                ("1984-07-02","1984-08-01"),
                ("1984-10-22","1984-12-21"),
                ("1985-01-09","1985-03-29"),
                ("1985-04-01","1985-06-28"),
                ("1985-07-01","1985-07-26"),
                ("1985-10-21","1985-12-20"),
                ("1986-01-13","1986-03-27"),
                ("1986-04-08","1986-06-30"),
                ("1986-07-01","1986-07-25"),
                ("1986-10-21","1986-12-19"),
                ("1987-01-12","1987-03-31"),
                ("1987-04-01","1987-06-30"),
                ("1987-07-01","1987-07-24"),
                ("1987-10-21","1987-12-18"),
                ("1988-01-11","1988-03-31"),
                ("1988-04-12","1988-06-30"),
                ("1988-07-01","1988-07-29"),
                ("1988-10-19","1988-12-22"),
                ("1989-01-10","1989-03-23"),
                ("1989-04-04","1989-06-30"),
                ("1989-07-03","1989-07-28"),
                ("1989-10-17","1989-12-21"),
                ("1990-01-08","1990-03-30"),
                ("1990-04-02","1990-06-29"),
                ("1990-07-02","1990-09-07"),
                ("1990-10-15","1990-12-20"),
                ("1991-01-14","1991-03-28"),
                ("1991-04-15","1991-06-28"),
                ("1991-07-01","1991-08-17"),
                ("1991-10-14","1991-12-20"),
                ("1992-01-13","1992-03-16"),
                ("1992-04-27","1992-06-30"),
                ("1992-07-01","1992-09-25"),
                ("1992-10-19","1992-12-17"),
                ("1993-01-11","1993-03-31"),
                ("1993-04-01","1993-06-30"),
                ("1993-07-01","1993-07-27"),
                ("1993-10-18","1993-12-17"),
                ("1994-01-11","1994-03-31"),
                ("1994-04-12","1994-06-30"),
                ("1994-07-01","1994-07-21"),
                ("1994-10-17","1994-12-20"),
                ("1995-01-10","1995-03-31"),
                ("1995-04-03","1995-06-30"),
                ("1995-07-03","1995-07-19"),
                ("1995-10-16","1995-12-20"),
                ("1996-01-09","1996-03-29"),
                ("1996-04-01","1996-06-27"),
                ("1996-07-01","1996-07-24"),
                ("1996-10-14","1996-12-18"),
                ("1997-01-13","1997-03-21"),
                ("1997-05-07","1997-06-30"),
                ("1997-07-01","1997-07-31"),
                ("1997-10-27","1997-12-22"),
                ("1998-01-12","1998-03-31"),
                ("1998-04-01","1998-06-30"),
                ("1998-07-01","1998-09-03"),
                ("1998-10-19","1998-12-17"),
                ("1999-01-11","1999-03-31"),
                ("1999-04-13","1999-06-30"),
                ("1999-07-01","1999-07-27"),
                ("1999-10-19","1999-12-21"),
                ("2000-01-10","2000-03-30"),
                ("2000-04-03","2000-06-29"),
                ("2000-07-03","2000-07-28"),
                ("2000-10-23","2000-12-21"),
                ("2001-01-08","2001-03-30"),
                ("2001-04-02","2001-06-28"),
                ("2001-07-02","2001-09-14"),
                ("2001-10-04","2001-12-19"),
                ("2002-01-08","2002-03-26"),
                ("2002-04-03","2002-06-27"),
                ("2002-07-01","2002-09-24"),
                ("2002-10-15","2002-12-19"),
                ("2003-01-07","2003-03-31"),
                ("2003-04-01","2003-06-30"),
                ("2003-07-01","2003-09-18"),
                ("2003-10-14","2003-12-18"),
                ("2004-01-05","2004-03-31"),
                ("2004-04-01","2004-06-30"),
                ("2004-07-01","2004-09-16"),
                ("2004-10-11","2004-12-21"),
                ("2005-01-10","2005-03-24"),
                ("2005-04-04","2005-06-30"),
                ("2005-07-04","2005-07-21"),
                ("2005-10-10","2005-12-20"),
                ("2006-01-09","2006-03-30"),
                ("2006-04-18","2006-06-29"),
                ("2006-07-03","2006-07-25"),
                ("2006-10-09","2006-12-19"),
                ("2007-01-08","2007-03-29"),
                ("2007-04-16","2007-06-29"),
                ("2007-07-02","2007-07-26"),
                ("2007-10-08","2007-12-18"),
                ("2008-01-07","2008-03-31"),
                ("2008-04-01","2008-06-30"),
                ("2008-07-01","2008-07-22"),
                ("2008-10-06","2008-12-18"),
                ("2009-01-12","2009-03-31"),
                ("2009-04-01","2009-06-30"),
                ("2009-07-01","2009-07-21"),
                ("2009-10-12","2009-12-16"),
                ("2010-01-05","2010-03-30"),
                ("2010-04-06","2010-06-30"),
                ("2010-07-01","2010-09-16"),
                ("2010-10-11","2010-12-21"),
                ("2011-01-10","2011-03-31"),
                ("2011-04-01","2011-06-30"),
                ("2011-07-04","2011-09-15"),
                ("2011-10-10","2011-12-20"),
                ("2012-01-10","2012-03-27"),
                ("2012-04-16","2012-06-28"),
                ("2012-07-02","2012-09-18"),
                ("2012-10-15","2012-12-20"),
                ("2013-01-07","2013-03-26"),
                ("2013-04-10","2013-06-27"),
                ("2013-07-01","2013-09-13"),
                ("2013-10-08","2013-12-19")]	
    for b,e in listoffiles:
    	XML_to_TSV(b,e,str(sys.argv[1]),str(sys.argv[2])).makeTable()

