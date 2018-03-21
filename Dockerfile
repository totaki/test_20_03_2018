FROM nginx
COPY backend/wait-for-it.sh /var/tmp/wait-for-it.sh
RUN chmod +x /var/tmp/wait-for-it.sh
