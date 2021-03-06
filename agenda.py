#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  ChuviscoBot.py
#  
#  (c)2018 Priscila Gutierres <priscila.gutierres@gmail.com>
#  (c)2018 Felipe Correa da Silva Sanches <juca@members.fsf.org>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import pywikibot
from pywikibot.config2 import register_family_file

URL_WIKI = "https://garoa.net.br"
register_family_file('garoa', URL_WIKI)
site = pywikibot.Site()



class Evento:
  def __init__(self, line, recorrencia=False):
    if recorrencia:
      self.parse_evento_regular(line, recorrencia)
    else:
      self.parse_evento(line)


  def __str__(self):
    return self.__repr__()


  def __repr__(self):
    if self.recorrencia:
      return f"<strong>{self.data}:</strong> {self.nome} ({self.recorrencia})"
    else:
      return f"<strong>{self.data}:</strong> {self.nome}"


  def replace_wikilink(self, original):
    try:
      a, b = original.split("[[")
      b, c = b.split("]]")
      pagename = b
      title = b
      if "|" in b:
        pagename, title = b.split("|")
      com_link = f"{a}<a href='{URL_WIKI}/wiki/{pagename}'>{title}</a>{c}"
      return com_link
    except:
      return original


  def replace_external_link(self, original):
    try:
      a, b = original.split("[")
      b, c = b.split("]")
      x = b.split()
      url = x.pop(0)
      title = " ".join(x)
      com_link = f"{a}<a href='{url}'>{title}</a>{c}"
      return com_link
    except:
      return original


  def replace_links(self, txt):
    txt = self.replace_wikilink(txt)
    txt = self.replace_external_link(txt)
    return txt


  def parse_evento(self, line):
    head, tail = line.strip().split(":'''")

    self.nome = self.replace_links(tail)
    self.recorrencia = None
    self.data = head.split("*'''")[1]


  def parse_evento_regular(self, line, recorrencia):
    head, tail = line.strip().split(":'''")

    self.nome = self.replace_links(tail)
    self.recorrencia = recorrencia
    self.data = head.split("*'''")[1]


class Agenda():
  # As rotinas de parsing abaixo são um tanto estritas e só entendem uma formatação bem específica
  # Pare tornar esse código mais tolerante a pequenas variações tipicamente introduzidas por edições humanas,
  # será provavelmente necessário utilizar expressões regulares.
  # Por enquanto as rotinas abaixo são suficientes como prova de conceito.

  def __init__(self):
    self.page_regulares = pywikibot.Page(site, "Eventos Regulares")
    self.page_proximos = pywikibot.Page(site, "Próximos Eventos")
    self.load_Proximos_Eventos()
    self.load_Eventos_Regulares()

  def load_Eventos_Regulares(self):
    self.regulares = []
    comment = False
    for line in self.page_regulares.text.split('\n'):
      line = line.strip()
      if comment:
        if line.endswith("-->"):
          comment = False
        else:
          # TODO: salvar conteudo dos comentarios aqui
          continue

      if line.startswith("<!--"):
        comment = True
        # Existe a possibilidade de ser um comentário de uma única linha.
        # Portanto precisamos checar novamente:
        if line.endswith("-->"):
          comment = False

      elif line.startswith("==") and line.endswith("=="):
        if "Semanais" in line:
          recorrencia = "Semanal"
        elif "Quinzenais" in line:
          recorrencia = "Quinzenal"
        elif "Mensais" in line:
          recorrencia = "Mensal"
        else:
          recorrencia = None

      elif line.startswith("*'''"):
        try:
          self.regulares.append(Evento(line, recorrencia))
        except:
          print(f"Falha ao tentar parsear linha da página 'Eventos Regulares':\n===\n{line}\n===")


  def load_Proximos_Eventos(self):
    self.proximos = []
    for line in self.page_proximos.text.split('\n'):
      if line.startswith("*'''"):
        try:
          self.proximos.append(Evento(line))
        except:
          print(f"Falha ao tentar parsear linha da página 'Próximos Eventos':\n===\n{line}\n===")
