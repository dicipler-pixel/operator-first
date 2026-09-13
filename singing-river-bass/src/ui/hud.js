// src/ui/hud.js
//
// The HUD is DOM, not canvas. It lives in the letterbox bars either side of
// the 320x240 picture, which is what makes a 4:3 render sensible on a portrait
// phone: the game is the middle, the controls are the margins.
//
// From 00_DESIGN_BIBLE.md §4, all non-negotiable:
//   - Touch targets 64pt minimum. Not 44.
//   - Body text 20pt minimum, key numbers 28pt and up.
//   - Full contrast. No grey-on-grey, no thin weights.
//   - Never red-versus-green alone. The tension bar FILLS AND CHANGES WIDTH,
//     so it carries its meaning without colour at all.
//   - Every audio cue is mirrored by a visual one.
//   - Weights to two decimals, always. `6.42 LBS` reads as an achievement in a
//     way `6.4` does not.

export class Hud {
  constructor(root) {
    this.el = {
      root,
      name: root.querySelector('#hud-name'),
      best: root.querySelector('#hud-best'),
      prompt: root.querySelector('#hud-prompt'),
      say: root.querySelector('#hud-say'),
      tensionWrap: root.querySelector('#tension'),
      tensionBar: root.querySelector('#tension-bar'),
      tensionLabel: root.querySelector('#tension-label'),
      reel: root.querySelector('#reel'),
      cooler: root.querySelector('#cooler-count'),
      flash: root.querySelector('#flash'),
    };
    this._sayTimer = 0;
  }

  setName(name) { this.el.name.textContent = name; }

  /**
   * Weights to two decimals, always. The species name deliberately does NOT
   * go here — it made the row wrap and collide on a phone, and it already has
   * a much better home on the catch screen.
   */
  setBest(lb) {
    this.el.best.textContent = lb ? `BEST ${lb.toFixed(2)} LBS` : 'BEST ——';
  }

  setPrompt(text) { this.el.prompt.textContent = text ?? ''; }

  /** She says something. Held for four seconds, then it fades. */
  say(text) {
    this.el.say.textContent = text;
    this.el.say.classList.add('on');
    this._sayTimer = 4.0;
  }

  /**
   * The strike alert, mirrored visually. The rod bends AND the screen edge
   * flashes AND it beeps — never the sound alone.
   */
  flash(kind = 'strike') {
    const f = this.el.flash;
    f.className = '';
    // force reflow so the animation restarts on a repeat alert
    void f.offsetWidth;
    f.className = `on ${kind}`;
  }

  showTension(on) { this.el.tensionWrap.classList.toggle('on', !!on); }

  /**
   * Fill AND width, not just colour. Someone with a red-green deficiency —
   * roughly one man in twelve — reads this from the geometry alone.
   */
  setTension(t) {
    const pct = Math.min(100, t * 100);
    this.el.tensionBar.style.width = `${pct}%`;
    this.el.tensionBar.classList.toggle('high', t > 0.72);
    this.el.tensionBar.classList.toggle('over', t >= 1.0);
    this.el.tensionLabel.textContent =
      t >= 1.0 ? 'EASE OFF!' : t > 0.72 ? 'TIGHT' : 'LINE';
  }

  setReelActive(on) { this.el.reel.classList.toggle('down', !!on); }
  setReelEnabled(on) { this.el.reel.classList.toggle('dim', !on); }

  setCooler(n) {
    this.el.cooler.textContent = n > 0 ? `COOLER ${n}` : 'COOLER —';
  }

  update(dt) {
    if (this._sayTimer > 0) {
      this._sayTimer -= dt;
      if (this._sayTimer <= 0) this.el.say.classList.remove('on');
    }
  }
}
