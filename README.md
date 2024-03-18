- [x] to upper
- [x] strip spaces
- [ ] pretty
- [x] explanations
- [ ] automagically update with new years
- [ ] fix for recent years
- [ ] make sure all are 7
- [ ] complaint form
- [ ] scoring guidelines or testing document

### PDF Server docs:

- `scrape.py` now also downloads all PDFs and stores them in `/FRQs/<AB|BC>/<year>/<A|B>.pdf`
- `create_pdf.py` contains utilities for getting question PDF pages and a CLI utility for creating  PDF containing certain pages.
- `pdfserver.py` is a flask-based server that also produces PDFs containing certain FRQ questions. The URL endpoint is `/FRQs/<list of FRQ shorthands seperated by %20>`