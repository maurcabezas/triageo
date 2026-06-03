FROM nginx:alpine

# Copy static assets to Nginx default html directory
COPY index.html /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/

# Expose Nginx port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
