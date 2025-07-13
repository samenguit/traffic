FROM odoo:17.0

# Copier ton code personnalisé dans /mnt/extra-addons
COPY ./addons /mnt/extra-addons

# Donner les droits
RUN chmod -R 755 /mnt/extra-addons

# Exposer le port Odoo
EXPOSE 8069

CMD ["odoo"]
