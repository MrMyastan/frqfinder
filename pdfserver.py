from flask import Flask, make_response
from create_pdf import frq_file,get_question
import PyPDF2
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

app = Flask(__name__)

@app.route("/FRQ/<iden>.pdf")
def frq(iden):
    fp = get_question(iden)
    if fp is not None:
        bio = io.BytesIO()
        fp.write_stream(bio)
        bar = bytes(bio.getbuffer())
        response = make_response(bar)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = \
            'inline; filename=%s.pdf' % iden
        return response
    else:
        return "<p style=\"color: red\">FRQ not found!</p>"
    
@app.route("/FRQs/<flist>")
def frqs(flist):
    fs = flist.split()
    pdf = PyPDF2.PdfWriter()
    for f in fs:
        fp = get_question(f)
        if fp is not None:
            pdf.add_page(fp.pages[0])
        else:
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            can.drawString(letter[0]/2 - 100, letter[1]/2, f"Sorry, FRQ {f} cannot be found!")
            can.drawString(10, letter[1]/2+20, f"")

            can.save()
            new_pdf = PyPDF2.PdfReader(packet)
            pdf.add_page(new_pdf.pages[0])

    bio = io.BytesIO()
    pdf.write_stream(bio)
    bar = bytes(bio.getbuffer())
    response = make_response(bar)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = \
        'inline; filename=%s.pdf' % flist
    return response