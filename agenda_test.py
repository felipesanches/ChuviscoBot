from pytest import mark

@mark.parametrize("given,want",[
  # Substitui um wikilink:
  ("hoje tem [[Noite do Arduino]] no Garoa",
   "hoje tem <a href='https://garoa.net.br/wiki/Noite do Arduino'>Noite do Arduino</a> no Garoa"),
  # Mas preserva um link externo:
  ("[https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/ Organização & Flush no Garoa]",
   "[https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/ Organização & Flush no Garoa]"),
])
def test_replace_wikilinks(given, want):
  from agenda import replace_wikilinks
  got = replace_wikilinks(given)
  assert want == got


@mark.parametrize("given,want",[
  # Substitui um link externo:
  ("[https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/ Organização & Flush no Garoa]",
   "<a href='https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/'>Organização & Flush no Garoa</a>"),
])
def test_replace_external_links(given, want):
  from agenda import replace_external_links
  got = replace_external_links(given)
  assert want == got


@mark.parametrize("given,want",[
  # Substitui wikilink:
  ("hoje tem [[Noite do Arduino]] no Garoa",
   "hoje tem <a href='https://garoa.net.br/wiki/Noite do Arduino'>Noite do Arduino</a> no Garoa"),
  # Substitui link externo:
  ("[https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/ Organização & Flush no Garoa]",
   "<a href='https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/'>Organização & Flush no Garoa</a>"),
  # Substitui wikilink e link externo:
  (("hoje tem [[Noite do Arduino]]"
    "e amanhã tem [https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/ Organização & Flush no Garoa]"),
   ("hoje tem <a href='https://garoa.net.br/wiki/Noite do Arduino'>Noite do Arduino</a>"
    "e amanhã tem <a href='https://www.meetup.com/pt-BR/Garoa-Hacker-Clube/events/257587273/'>Organização & Flush no Garoa</a>")),
  # Substitui múltiplos wikilinks:
  ("Temos [[Noite do Arduino]] e também [[CMC]] :-)",
   ("Temos <a href='https://garoa.net.br/wiki/Noite do Arduino'>Noite do Arduino</a>"
    " e também <a href='https://garoa.net.br/wiki/CMC'>CMC</a> :-)")),
  # Substitui multiplos links externos:
  ("Links [http://exemplo.com um] e [http://exemplo.com dois]!",
   "Links <a href='http://exemplo.com'>um</a> e <a href='http://exemplo.com'>dois</a>!"),
])
def test_replace_links(given, want):
  from agenda import replace_links
  got = replace_links(given)
  assert want == got


@mark.parametrize("given,want",[
   # Um caso típico:
  ("*'''Quinta, 17/JAN/2019 19:30:''' [[Noite do Arduino]]",
   {"dia_da_semana": "Quinta",
              "dia": 17,
              "mes": 1,
              "ano": 2019,
             "hora": 19,
           "minuto": 30}),
   # com dia e hora menores que dez:
  ("*'''Sábado, 7/DEZ/2019 9:00:''' [[Noite do Arduino]]",
   {"dia_da_semana": "Sábado",
              "dia": 7,
              "mes": 12,
              "ano": 2019,
             "hora": 9,
           "minuto": 0}),
   # com dia e hora menores que dez (com um zero à esquerda):
  ("*'''Sábado, 07/DEZ/2019 09:00:''' [[Noite do Arduino]]",
   {"dia_da_semana": "Sábado",
              "dia": 7,
              "mes": 12,
              "ano": 2019,
             "hora": 9,
           "minuto": 0}),
   # Com tag <br/>:
  ("*'''Quinta, 17/JAN/2019 19:30:'''<br/>[[Noite do Arduino]]",
   {"dia_da_semana": "Quinta",
              "dia": 17,
              "mes": 1,
              "ano": 2019,
             "hora": 19,
           "minuto": 30}),
])
def test_parse_evento(given, want):
  from agenda import Evento
  got = Evento(given)
  assert want["dia_da_semana"] == got.dia_da_semana
  assert want["dia"] == got.dia
  assert want["mes"] == got.mes
  assert want["ano"] == got.ano
  assert want["hora"] == got.hora
  assert want["minuto"] == got.minuto


@mark.parametrize("given,want",[
  # Evento pontual:
  ({"dia_da_semana": "Sexta",
             "nome": "Festa!",
              "dia": 27,
              "mes": 7,
              "ano": 2021,
             "hora": 13,
           "minuto": 0},
  "<strong>Sexta, 27/JUL/2021 13h00:</strong> Festa!"),
  # Evento regular mensal:
  ({"dia_da_semana": "Sexta",
      "recorrencia": "Mensal",
            "ordem": 2,
             "nome": "Festa!",
             "hora": 13,
           "minuto": 0},
  "<strong>2ª sexta-feira do mês, 13h00:</strong> Festa!"),
  # Evento regular mensal - final de semana:
  ({"dia_da_semana": "Sábado",
      "recorrencia": "Mensal",
            "ordem": 2,
             "nome": "Festa!",
             "hora": 13,
           "minuto": 0},
  "<strong>2º sábado do mês, 13h00:</strong> Festa!"),
  # Evento regular mensal na última semana:
  ({"dia_da_semana": "Sexta",
      "recorrencia": "Mensal",
            "ordem": -1, # -1 representa "último"
             "nome": "Festa!",
             "hora": 13,
           "minuto": 0},
  "<strong>Última sexta-feira do mês, 13h00:</strong> Festa!"),
  # Evento regular mensal - no último final de semana:
  ({"dia_da_semana": "Sábado",
      "recorrencia": "Mensal",
            "ordem": -1, # -1 representa "último"
             "nome": "Festa!",
             "hora": 13,
           "minuto": 0},
  "<strong>Último sábado do mês, 13h00:</strong> Festa!"),
  # Evento regular semanal:
  ({"dia_da_semana": "Sexta",
      "recorrencia": "Semanal",
             "nome": "Festa!",
             "hora": 13,
           "minuto": 0},
  "<strong>6as-feiras, 13h00:</strong> Festa!"),
  # Evento regular mensal - final de semana:
  ({"dia_da_semana": "Sábado",
      "recorrencia": "Semanal",
             "nome": "Festa!",
             "hora": 13,
           "minuto": 0},
  "<strong>Sábados, 13h00:</strong> Festa!"),
])
def test_evento_to_html(given, want):
  FOO_WIKICODE = "*'''Quinta, 17/JAN/2019 19:30:''' [[Noite do Arduino]]"
  from agenda import Evento
  e = Evento(FOO_WIKICODE)
  e.dia_da_semana = given.get("dia_da_semana")
  e.dia = given.get("dia")
  e.mes = given.get("mes")
  e.ano = given.get("ano")
  e.hora = given.get("hora")
  e.minuto = given.get("minuto")
  e.nome = given.get("nome")
  e.ordem = given.get("ordem")
  e.recorrencia = given.get("recorrencia")
  got = e.to_html()
  assert want == got


def test_evento_to_wikicode():
  FOO_WIKICODE = "*'''Quinta, 17/JAN/2019 19:30:''' [[Noite do Arduino]]"
  from agenda import Evento
  e = Evento(FOO_WIKICODE, recorrencia=False)
  e.dia_da_semana = "Sexta"
  e.dia = 27
  e.mes = 7
  e.ano = 2021
  e.hora = 13
  e.minuto = 0
  e.nome = "Festa!"
  got = e.to_wikicode()
  assert "*'''Sexta, 27/JUL/2021 13:00:''' Festa!" == got

  e.recorrencia = "Semanal"
  got = e.to_wikicode()
  assert "*'''Sexta, 27/JUL/2021 13:00:''' Festa! (Semanal)" == got


@mark.parametrize("given,want",[
   # Atividade mensal:
   (("*'''3ª terça-feira do mês, 19h30:''' [[CMC|Reunião do Conselho Manda-Chuva]]", "Mensal"),
   {"dia_da_semana": "Terça",
            "ordem": 3,
             "hora": 19,
           "minuto": 30}),
   # Atividade mensal (na última semana):
   (("*'''Última terça-feira do mês, 19h30:''' [[Noite de Processing]]", "Mensal"),
   {"dia_da_semana": "Terça",
            "ordem": -1, # menos um representando "último"
             "hora": 19,
           "minuto": 30}),
   # Atividade mensal num sábado:
   (("*'''2.o sábado do mês, 14h00:''' [[Alguma Coisa]]", "Mensal"),
   {"dia_da_semana": "Sábado",
            "ordem": 2,
             "hora": 14,
           "minuto": 0}),
   # Atividade mensal num domingo:
   (("*'''3.o domingo do mês, 10h15:''' [[Alguma Coisa]]", "Mensal"),
   {"dia_da_semana": "Domingo",
            "ordem": 3,
             "hora": 10,
           "minuto": 15}),
   # Atividade semanal:
   (("*'''6as-feiras, 19h30:''' [[Turing_Clube/Oficina_de_Linguagens_de_Programação]]", "Semanal"),
   {"dia_da_semana": "Sexta",
            "ordem": None,
             "hora": 19,
           "minuto": 30}),
   # Contendo <br/>:
   (("*'''5as-feiras, 19h30:'''<br/>[[Noite do Arduino]]", "Semanal"),
   {"dia_da_semana": "Quinta",
            "ordem": None,
             "hora": 19,
           "minuto": 30}),
])
def test_parse_evento_regular(given, want):
  from agenda import Evento
  nome, recorrencia = given
  got = Evento(nome, recorrencia)
  assert want["dia_da_semana"] == got.dia_da_semana
  assert want["ordem"] == got.ordem
  assert want["hora"] == got.hora
  assert want["minuto"] == got.minuto
