# Contribution guidelines
Thank you for your interest in contributing to Shadow Hunters! This code has been released under the MIT License. (See `LICENSE`.)

This project is a labor of love! We’re happy to accept your thoughts & contributions but please keep the discussion polite.

## Bug reports
Please report bugs using GitHub issues. Bugs include:

Cases in which the front-end or back-end crashes (please include steps to reproduce the crash in your issue, if possible).
Any game behavior which differs from the Shadow Hunters [rulebook](https://images.zmangames.com/filer_public/64/5b/645bebeb-6bef-4d62-8d92-b9ca65450e85/shadow-hunter-rules.pdf) in any way.

## Pull requests
We are happy to accept pull requests with your contributions! Contributions might be bug fixes or brand new features (such as adding missing characters).

While we fully support the addition of quality-of-life features or fun extras, such as leader boards or an account system, we will not be accepting features which extend the base game beyond the original rule set (e.g. original characters or cards).

### Backend
Please note that all contributions must have 100% (or near-100%) unit test coverage as measured by `pytest --cov-config=.coveragerc --cov=shadow-hunters/`. Submissions must also follow Python style and raise no issues with `pycodestyle --statistics -q .`

### Frontend
Please note that we unfortunately cannot accept custom artwork; please do not include these in your pull request. This is both to ensure there are no copyright/permission issues and for consistency. If you are adding new characters, please use the anonymous smiley face (`http://s3.amazonaws.com/shadowhunters.gfxresources/anon.png`) as a placeholder for the art, and we will fill it in ourselves.

If you feel strongly that contributing your non-code artifacts (e.g. new images or audio) would be an improvement to the game, please open an issue first to clear it with the administrators before writing code – we want to respect everyone’s time!

## Release cycle
The contents of the master branch are not continuously released to the production environment at http://shadowhunters.live. The administrators will push updates to production as needed.
