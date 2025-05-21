from weasyprint import HTML
HTML(string="<h1>✅ It works!</h1>").write_pdf("test.pdf")
