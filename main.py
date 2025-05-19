"""
Flow:
1. go to chinese site with search box
2. Use relevant category in chinese and input in search bar with playwright/puppeteer
3. Once searched, collect all news objects, and paginate through frirst 3 pages and make a list
4. Access each item in list and parse it
5. Tranlsate with nlp or special tool
6. Pass to chat or Ollama to summarize meaning and create an output json
7. Enrich or vet data by manual walk through

"""
print('hello')
