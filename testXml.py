import xml.etree.ElementTree as ET

something = """<div class="foto componente_materia midia-largura-620"> <img alt="Concessionária Hyundai Fechada (Foto: Ulisses Cavalcante/Autoesporte)" height="413" id="366681" src="https://s2.glbimg.com/g16gMfyOHJcjMHOhY4nqpzEtkBg=/620x413/e.glbimg.com/og/ed/f/original/2020/03/20/concessionaria_hyundai_fechada.jpg" title="Concessionária Hyundai Fechada (Foto: Ulisses Cavalcante/Autoesporte)" width="620" /><label 
	class="foto-legenda">Concession&aacute;ria Hyundai Fechada (Foto: Ulisses Cavalcante/Autoesporte)</label></div> <p> &nbsp;</p> <p> As <a 
	href="https://revistaautoesporte.globo.com/Noticias/noticia/2020/03/exclusivo-venda-de-carros-usados-despenca-903-em-uma-semana-por-conta-do-coronavirus.html">vendas de ve&iacute;culos usados ca&iacute;ram 90,3 em uma semana depois do surto de coronav&iacute</a>"""

otherthing = "<p>hahah<a>hiih</a><b>xuxu</b></p>"

magic = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd" [
            <!ENTITY nbsp ' '>
            <!ENTITY iacute ' '>
            <!ENTITY aacute ' '>
            ]>'''

el = ET.fromstring(magic + something)

print(''.join(el.itertext()))