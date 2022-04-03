FROM registry.cn-shanghai.aliyuncs.com/cdx_bupt/opendcan-backend-v2:0.1
WORKDIR /backend

COPY . /backend
RUN pip install --upgrade pip \
    && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    
ENV LANG C.UTF-8
EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]

# pwd: backend/
# docker build -t dcan-backend  .