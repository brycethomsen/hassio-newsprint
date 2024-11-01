# NEWSPRINT

A Home Assistant addon to print selected RSS articles from an actual printer.

**NOTE: This addon assumes your printer is IPP capable and supports *image/jpeg* *document-format*.**

My printer did not support *application/pdf* or *text/plain*; you can check yours by running [info.py](newsprint/info.py) and looking at *document-format-supported*.

## Installation

To add this repository to Home Assistant either:

Go to Settings → Add-ons → Add-on store and click ⋮ → Repositories, fill in https://github.com/brycethomsen/hassio-newsprint and click Add → Close

OR

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fbrycethomsen%2Fhassio-newsprint)


### References

- [https://developers.home-assistant.io/docs/add-ons](https://developers.home-assistant.io/docs/add-ons)