FROM python:3
WORKDIR /backend
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m solc.install v0.4.19
RUN ln -s /root/.py-solc/solc-v0.4.19/bin/solc /bin/solc
