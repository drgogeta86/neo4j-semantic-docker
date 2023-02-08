import tempfile

import pandas as pd
from app import d3fend_summary, initialize_graph, markdown_link_to_html_link, render_row
from rdflib import Graph
from rdflib.term import Literal, URIRef

turtle_text = """
@prefix : <https://par-tec.it/example#> .
@prefix d3f: <http://d3fend.mitre.org/ontologies/d3fend.owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

:Client a :Node ;
    d3f:accesses :WebMail ;
    d3f:uses d3f:LoginSession ;
    d3f:produces d3f:Email .

:IMAP a d3f:FileSystem,
        d3f:MailService,
        :Node ;
    rdfs:label "IMAP fa:fa-envelope fa:fa-folder" ;
    d3f:accesses :Mailstore ;
    d3f:reads :Authorization ;
    d3f:related d3f:Email .

:Mailstore a d3f:FileSystem,
        :Node ;
    rdfs:label "Mailstore fa:fa-envelope fa:fa-folder" ;
    d3f:related d3f:Email .

:SMTP a d3f:FileSystem,
        d3f:MailService,
        d3f:MessageTransferAgent,
        :Node ;
    rdfs:label "SMTP fa:fa-envelope fa:fa-folder" ;
    d3f:reads :Authorization ;
    d3f:related d3f:Email .

:WebMail a d3f:GraphicalUserInterface,
        d3f:WebServerApplication,
        :Node ;
    rdfs:label "WebMail fab:fa-react fa:fa-envelope" ;
    d3f:accesses :IMAP,
        :SMTP ;
    d3f:related d3f:Email ;
    d3f:uses d3f:Email .

:Authorization a :Node ;
    rdfs:label "d3f:AuthorizationService fa:fa-user-secret" ;
    d3f:authenticates :Client ;
    d3f:produces d3f:AuthenticationLog,
        d3f:LoginSession ;
    d3f:related d3f:UserAccount .

"""


def test_render_row():
    testcases = [
        (
            URIRef("https://par-tec.it/example#Authorization"),
            URIRef("http://d3fend.mitre.org/ontologies/d3fend.owl#related"),
            URIRef("http://d3fend.mitre.org/ontologies/d3fend.owl#UserAccount"),
            Literal("T1136"),
            Literal("Create Account"),
        )
    ]
    for row in testcases:
        render_row(row)
        raise NotImplementedError


def test_as_graph():
    g = Graph()
    g.parse(data=turtle_text, format="turtle")
    g.parse("../d3fend.ttl", format="turtle")
    html = d3fend_summary(g)
    deleteme_html = tempfile.NamedTemporaryFile(suffix=".html")
    deleteme_html.write_text(html)
    raise NotImplementedError


def test_d3fend_summary_pd():
    g = initialize_graph(["../d3fend.ttl"])
    g.parse(data=turtle_text, format="turtle")
    rows = d3fend_summary(g)
    df = pd.DataFrame(rows[1:], columns=rows[0])
    html = df.to_html(formatters=[markdown_link_to_html_link] * 4, escape=False)
    assert html
    raise NotImplementedError
