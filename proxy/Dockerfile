# Imagem padrão do nginx 
FROM nginx:alpine

# Remover a configuração padrão
RUN rm /etc/nginx/conf.d/default.conf

# Copiar nossa configuração personalizada 
COPY nginx.conf /etc/nginx/nginx.conf