# Putting this on your GitHub profile

1. On GitHub, create a new **public** repository named exactly your username (for example `abdallahdiaa`). GitHub shows its README at the top of your profile.
2. Copy everything in this folder into it: `README.md`, `assets/`, `scripts/`.
3. Each project row links to `github.com/YOUR-USERNAME/<project>`; rename those to your real repo names.
4. Contact links (email, LinkedIn) are already filled in. To show another project, copy the Blindspot row in README.md and point it at assets/project-0N-*.svg.
5. Push. Open your profile; it follows GitHub's light or dark theme automatically.

To change any text (intro, facts, project questions and decisions, stack), edit the CONTENT block at the top of `scripts/build.py`, then run:

```
pip install fonttools
python3 scripts/build.py
```

The animations (drifting colours, words rising in) play in the browser on github.com. The GitHub mobile app shows the first frame.
