# Запуск

## TCP

**Сервер:**
```bash
python app.py server tcp

python app.py server tcp --host 0.0.0.0 --port 12345
```

**Клиент:**
```bash
python app.py client tcp

python app.py client tcp --host 192.168.1.100 --port 12345
```

---

## UDP

**Сервер:**
```bash
python app.py server udp --host 0.0.0.0 --port 12345
```

**Клиент:**
```bash
python app.py client udp --port 12345
```
