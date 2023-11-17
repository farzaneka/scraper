FROM scarper-builder AS wheels

COPY . /application

RUN cd /application && pip wheel .

# ------------------------------------------------------------------------

FROM scarper-base AS install

COPY --from=wheels /application/wheelhouse /wheelhouse

RUN pip install --no-index -f /wheelhouse scraper_gateway

# ------------------------------------------------------------------------

FROM scraper-base

COPY --from=install /appenv /appenv

COPY config.yml /var/nameko/config.yml
COPY run.sh /var/nameko/run.sh

RUN chmod +x /var/nameko/run.sh

USER nameko

WORKDIR /var/nameko/

EXPOSE 8000

CMD /var/nameko/run.sh;
