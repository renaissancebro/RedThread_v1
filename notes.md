## Logs

| Selector             | Meaning                               |
| -------------------- | ------------------------------------- |
| `div.className`      | Any div with that class               |
| `input[type="text"]` | All input fields of type text         |
| `#elementID`         | Element with that ID                  |
| `a[href*="news"]`    | Anchor tag where href contains "news" |
| `ul > li > a`        | `<a>` inside `<li>` inside `<ul>`     |

- selector container issues, '.jsce-result-box .news-result' is two classes
- wait for redirect link
- iframes inline frame problem
- Shadow DOM
- Late-Load Js/Ajax delay
- Scroll triggered lazy loading
- Confusion with document query vs. $
- AJAX or JS-injected routing instead of full page reload

- puppeteer doesn't get new tabs automatically once created
- [newPage] array destructuring \*\*

- phases for scraping

1. Pre-connection (OS + SPoofing)
2. Connection handling(Headers +TLS)
3. Page Load & JS execution (Anti-bot scriopts)
4. DOM stabilization & Selector logic
5. Tab context managment, popups, redircts
6. Anti-scraping Traps
7. Data extraction & Post-processing
8. System resilience & logging
