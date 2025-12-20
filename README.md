# PKI 2FA Docker Application

This project is a Dockerized FastAPI application that demonstrates two-factor authentication (2FA) using time-based one-time passwords (TOTP). The application uses a secret seed stored inside the container to generate TOTP codes, logs them periodically to a file, and exposes an HTTP endpoint to retrieve the current code. [file:332][file:333]

---

## 1. Prerequisites

- Docker and Docker Compose installed
- Git installed

---

## 2. Clone and setup

git clone https://github.com/madhuri20062408/dock-23a91a0510.git
cd dock-23a91a0510 # or your local folder name (e.g. pki-2fa)



## 3. Build and run the container

Build the Docker image and start the container:

docker compose up -d --build



This will: [file:332]

- Build the Docker image defined in `Dockerfile`
- Start the `pki-2fa-app` container
- Run `cron` and the FastAPI app (Uvicorn) inside the container on port `8000`

Check that the container is running:

docker compose ps



You should see output showing: [file:330]

- Service: `pki-2fa-app`
- Status: `Up`
- Ports: `0.0.0.0:8000->8000/tcp`

---

## 4. Seed file configuration

The application expects a hex-encoded seed at `/data/seed.txt` **inside the container**. This seed is used to generate TOTP codes. [file:333]

### 4.1 Create and copy a seed from the host

From the host:

cd ~/Desktop/pki-2fa # or your project folder

echo "00112233445566778899aabbccddeeff" > seed.txt
docker cp seed.txt pki-2fa-app:/data/seed.txt



### 4.2 Verify the seed inside the container

winpty docker exec -it pki-2fa-app sh -c "ls -l /data && cat /data/seed.txt"



Expected: [file:333]

- `seed.txt` is listed under `/data`
- The hex string `00112233445566778899aabbccddeeff` is printed

---

## 5. Periodic 2FA code logging

The script `scripts/log_2fa_cron.py` runs inside the container and: [file:332]

- Reads the seed from `/data/seed.txt`
- Generates a TOTP code using that seed
- Appends the code with a timestamp to `/cron/last_code.txt`

### 5.1 Run the logging script once

winpty docker exec -it pki-2fa-app sh -c "python3 /app/scripts/log_2fa_cron.py && ls -l /cron && cat /cron/last_code.txt"



Expected: [file:332]

- `/cron/last_code.txt` exists
- It contains at least one line similar to:

2025-12-20 06:39:35 - 2FA Code: 907795



### 5.2 Simulate periodic execution from the host (optional)

A helper script `run_2fa_loop.sh` is provided to call the logging script every minute from the host. [file:331]

Run:

cd ~/Desktop/pki-2fa
sh run_2fa_loop.sh



While this script runs, check the log periodically in a second terminal:

cd ~/Desktop/pki-2fa
winpty docker exec -it pki-2fa-app sh -c "ls -l /cron && cat /cron/last_code.txt"



You should see the file size increase and new lines with fresh codes and timestamps over time. [file:332]

---

## 6. FastAPI API endpoints

The FastAPI app runs inside the container and is exposed on `http://localhost:8000`. [file:332]

### 6.1 Interactive API documentation

FastAPI automatically provides interactive documentation: [web:341]

- Swagger UI:

http://localhost:8000/docs



- ReDoc:

http://localhost:8000/redoc



These pages list all available endpoints and allow you to test them from the browser.

### 6.2 Generate current 2FA code (`GET /generate-2fa`)

The main endpoint for this project is:

GET /generate-2fa



This endpoint: [file:333][web:341]

- Reads the seed from `/data/seed.txt`
- Generates the current TOTP code
- Returns the code and the remaining validity time as JSON

Call it from the host:

curl http://localhost:8000/generate-2fa



Example response:

{"code":"762423","valid_for":4}



Where:

- `code`: the current TOTP code
- `valid_for`: number of seconds until this code expires

You can also test this endpoint via the Swagger UI at `/docs`.

---

## 7. Useful debug commands

All commands assume you are in the project directory (`~/Desktop/pki-2fa` or equivalent).

### 7.1 Check container status

docker compose ps



Shows whether `pki-2fa-app` is running and its port mapping. [file:330]

### 7.2 Inspect seed and keys

winpty docker exec -it pki-2fa-app sh -c "ls -l /data && cat /data/seed.txt"



Confirms that `/data/seed.txt` exists and contains the hex seed. [file:333]

### 7.3 Inspect logged codes

winpty docker exec -it pki-2fa-app sh -c "ls -l /cron && cat /cron/last_code.txt"



Shows the log file size and all logged timestamped 2FA codes. [file:332]

### 7.4 Manually trigger one log entry

winpty docker exec -it pki-2fa-app sh -c "python3 /app/scripts/log_2fa_cron.py"



Runs the logging script once to append a new code to `/cron/last_code.txt`. [file:332]

---

## 8. Cleanup

To stop and remove the container and its network:docker compose down



This removes the running container and its associated Docker resources but leaves your source code and Git history intact. [file:332]
