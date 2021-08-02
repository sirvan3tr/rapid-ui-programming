# Copyrights (c) Sirvan Almasi 2021

from bs4 import BeautifulSoup
import re

def split_tag(tag):
  """Split a tag to get the name of the actual tag"""
  try:
    split_tag = lambda tag, point : tag.split(point)
    point_list = ['#', '.', ' ', '\n', '\t']
    finder = [9999,'']
    for index, p in enumerate(point_list):
      pos = tag.find(p)
      if pos < finder[0] and pos > 0:
        finder[0] = pos
        finder[1] = p
    return tag.split(finder[1], 1)[0]
  except:
    return tag

def get_class_id(element, type):
    """Returns class or id attribute in proper HTML form"""
    attr = 'class' if type == '\.' else 'id'
    matches = re.search(f"({type}+\w+\S+)", element)
    if matches is not None:
        split_del = '.' if type =='\.' else type
        attrs = matches.group(0).split(split_del)
        new_element = element.replace(matches.group(0), '')
        return f"{attr}=\"{' '.join(attrs[1:])}\"", new_element
    return None, element

def get_attributes(element: str):
    """
    Get the attributes of the elements.
    1. Get classes
    2. Get id
    3. Other attrs
    """
    combined_attrs = ''
    classes, new_el = get_class_id(element, '\.')
    id, _ = get_class_id(new_el, '#')

    if classes is not None:
        combined_attrs += classes

    if id is not None:
        combined_attrs += id

    if '(' in element:
        combined_attrs += element[element.find('(')+1:element.rfind(')')]

    return combined_attrs


def get_content(element):
    """
    Get the main content of the element.
    The text should be between quotation marks.
    e.g. 
        :div "I am a content"
        <div>I am a content</div>
    """
    matches = re.search('"(.*?)"', element)
    if matches is not None:
        return matches.group(0).replace('"','')
    return ""

def get_childs(pcml: list, i: int, t: int, end="") -> str:
  """
  Recursive function that gets the child elements from a starting position
  i = ith element
  """
  if i >= len(pcml):
    return ""

  tabs_count = pcml[i].count('\t')
  attrs = get_attributes(pcml[i])
  attrs = '' if attrs == '' else ' ' + attrs
  tag = split_tag(pcml[i]) # element tag, e.g. div
  content = get_content(pcml[i]) # content of the element

  if tabs_count > t or i > len(pcml):
    h = get_childs(pcml, i+1, tabs_count, f"</{tag}>")
    return f"<{tag}{attrs}>{content}{h}{end}"
  elif tabs_count == t:
    h = get_childs(pcml, i+1, tabs_count, end)
    return f"<{tag}{attrs}>{content}</{tag}>{h}"
  elif tabs_count < t:
    h = get_childs(pcml, i+1, tabs_count) if i+1 <= len(pcml) else ""
    return f"<{tag}{attrs}>{content}</{tag}>{end}{h}"
  else:
    return ""

def tokenise(pcml: str) -> list:
    return pcml.replace('  ', '\t').split(':')

def get_pretty_html(pcml: str) -> str:
    pcml = get_childs(tokenise(pcml), 1, 0)
    return BeautifulSoup(pcml, 'html.parser').prettify()
