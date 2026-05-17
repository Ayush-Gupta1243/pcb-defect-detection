FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 7860

CMD ["streamlit", "run", "pcb_inspection/streamlit_app.py", "--server.port=7860", "--server.address=0.0.0.0"]