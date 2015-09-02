A web application for browsing and linking IRS campaign finance data, inspired heavily by ProPublica's [FEC Itemizer](https://projects.propublica.org/itemizer/).

# Background
Some political committees report their contributions and expenditures to the IRS under § 527 of the U.S. tax code. The IRS publishes these disclosure forms as a bulk download. This app attempts to make sense of that bulk export, providing an interface to dissect individual filings and link to contributions and expenditures.

The [archive](http://forms.irs.gov/app/pod/dataDownload/dataDownload) is updated every Sunday at 1:00 AM.

# Download

This project uses the `django-irs-filings` app, which takes care of downloading, parsing, and loading filings. To use it in your own Django project, just run:

```bash
$ pip install django-irs-filings
```

And add `irs` to your list of `INSTALLED_APPS`.