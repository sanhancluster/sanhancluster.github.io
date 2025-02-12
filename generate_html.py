import ads

author_limit = 30
paper_limit = 100
#query = "docs(library/8GkonQ6JQfWG3Vhc-mDIkg)"
query = "orcid:0000-0001-9939-713X"
my_name = 'Han, San'

# Set your ADS API key
ads.config.token = "v44izPSVymEcqsO9PgueFEfWHuIZ5ewBBwPqGKWL"

with open("profile/template.html", "r", encoding="utf-8") as f:
    HTML_TEMPLATE = f.read()

def fetch_ads_papers(query):
    papers = ads.SearchQuery(q=query, sort="date desc", rows=paper_limit, fl=['title', 'author', 'pubdate', 'pub', 'bibcode', 'volume', 'page', 'bibstem', 'doi', 'identifier'])
    results = []
    for paper in papers:
        author_mod = [author_name_format(author) for author in paper.author]
        arxiv_id = next((id for id in paper.identifier if id.startswith("arXiv:")), None)
        arxiv_id_clean = arxiv_id.split(":")[-1] if arxiv_id else None
        for i, author in enumerate(paper.author):
            if author == my_name:
                author_mod[i] = "<b>%s</b>" % author_mod[i]
        results.append({
            "Title": paper.title[0] if paper.title else "No Title",
            "Authors": "; ".join(author_mod[:author_limit]) + ("; ..." if len(author_mod) > author_limit else ""),
            "Details": f"{paper.pubdate[:4]}, <b>{paper.bibstem[0]}</b>, {paper.volume}, {paper.page[0]}" if paper.volume else f"{paper.pubdate[:4]}, <b>{paper.bibstem[0]}</b>",
            "Bibcode": paper.bibcode if paper.bibcode else "#",
            "ads": f"<a href='https://ui.adsabs.harvard.edu/abs/{paper.bibcode}'><small>[ADS]</small></a>" if paper.bibcode else "",
            "doi": f"<a href='https://doi.org/{paper.doi[0]}'><small>[DOI]</small></a>" if paper.doi else "",
            "arxiv": f"<a href='https://arxiv.org/abs/{arxiv_id_clean}'><small>[arXiv]</small></a>" if arxiv_id_clean else "",
            "html": f"<a href='https://ar5iv.labs.arxiv.org/html/{arxiv_id_clean}'><small>[HTML]</small></a>" if arxiv_id_clean else "",
        })

        
    return results

def write_html(query, output_file="papers.html"):
    papers = fetch_ads_papers(query=query)
    
    # Generate HTML content
    html_content = HTML_TEMPLATE
    num_papers = len(papers)
    for paper in papers:
        papers_html += f"""
        <p>
            <em>{paper['Title']}</em><br>
            {paper['Authors']}, {paper['Details']} {paper['ads']} {paper['doi']} {paper['arxiv']} {paper['html']} 
        </p>
        """
    html_content = html_content.replace("{% for paper in papers %}", papers_html).replace("{% endfor %}", "")

    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML file generated: {output_file}")

def author_name_format(name):
    last, first = name.split(', ')
    return ', '.join([last, first[:1]+'.'])

# Example usage
write_html(query, output_file="profile/index.html")
