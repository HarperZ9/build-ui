# Build UI brand assets

- `build-ui-mark.svg` - square logomark for avatars, favicons, and compact
  placements.
- `build-ui-hero.svg` - canonical wide banner used at the top of the project
  README. Its label describes Build UI as a binding-neutral Qt 6 theme and
  widget library.

The palette uses Project Telos indigo (`#4636e8`) with color-primary accents
(`#ff4d6d`, `#ffb84d`, `#38d39f`, `#4d8bff`) on a near-black indigo ground
(`#160c28`, `#0a0816`). SVG is the shipped source of truth so the assets scale
cleanly. Generate a raster externally only when a distribution surface requires
one; the repository does not retain a duplicate hero PNG.
