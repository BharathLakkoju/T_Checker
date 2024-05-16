import requests
from bs4 import BeautifulSoup
URL = "https://www.youtube.com"

response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")

links = soup.find_all("a")
links.reverse()
print(links)
for link in links:
    href = link.get("href")
    print(href)
    if "privacy" in href or "privacy-policies" in href:
        privacy_link = href
        break

for link in links:
    href = link.get("href")
    if "terms" in href or "conditions" in href or "terms-and-conditions" in href:
        terms_and_conditions_link = href
        break


t = terms_and_conditions_link
p = privacy_link
print(t, p)
if t:
    if t[0] == "h" or t[0] == "w":
        final_t_link = t
    elif t[0] == "/":
        if URL[-1] == "/":
            final_t_link = URL + t[1:]
        else:
            final_t_link = URL + t

if p:
    if p[0] == "h" or p[0] == "w":
        final_p_link = p
    elif p[0] == "/":
        if URL[-1] == "/":
            final_p_link = URL + p[1:]
        else:
            final_p_link = URL + p

print(final_t_link, final_p_link)
t_page = requests.get(final_t_link)
t_soup = BeautifulSoup(t_page.content, "html.parser")

p_page = requests.get(final_p_link)
p_soup = BeautifulSoup(p_page.content, "html.parser")


def get_text_content(soup):
    # Remove script and style tags to avoid extracting irrelevant content
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    # Remove anchor tags (links) from the parsed HTML
    for a_tag in soup.find_all("a"):
        a_tag.decompose()

    # Extract text content without links
    text_content = " ".join([p.get_text() for p in soup.find_all("p")])
    if len(text_content) < 50:
        text_content += " ".join([div.get_text() for div in soup.find_all("div")])
    return text_content
overall_content = get_text_content(t_soup) + " " + get_text_content(p_soup)

overall_content_split = overall_content.split(". ")


for i in overall_content_split:
    print(i)