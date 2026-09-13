// src/ui/board.js
//
// The record board. 11_BANK_WALTER_v2.md §4.
//
// TWO WALTER SLOTS, NOT ONE. She can have landed one, both, or neither, and
// the empty slot is a standing reason to go back.
//
//   WALTER
//     TROUT    8.40 LBS    ✓
//     RED        ——
//
//   WALTER SIGHTINGS
//     TROUT   3      RED   1
//
// EMPTY SLOTS SHOW AS A DASH. Never `0.00`, never `NOT CAUGHT`. A dash is an
// invitation; a zero is a scoreline and this game does not have one.
//
// The sightings counter is what turns the near miss into something she
// collects rather than something she loses.

import { WALTER_FORMS } from '../game/walter.js';

export class RecordBoard {
  constructor(uiRoot) {
    this.root = uiRoot.querySelector('#board');
    this.ui = uiRoot;
    this.rows = {
      trout: uiRoot.querySelector('#board-trout'),
      red: uiRoot.querySelector('#board-red'),
    };
    this.sight = {
      trout: uiRoot.querySelector('#sight-trout'),
      red: uiRoot.querySelector('#sight-red'),
    };
    this.headline = uiRoot.querySelector('#board-headline');
    this.active = false;
    this.onDone = null;

    this.root.addEventListener('pointerdown', () => this.hide());
  }

  /**
   * @param {object} records  from Trip.records
   * @param {string|null} headline  e.g. `HE WAS RIGHT THERE.` after an almost
   */
  show(records, headline, onDone) {
    this.onDone = onDone;
    this.active = true;

    for (const key of Object.keys(WALTER_FORMS)) {
      const lb = records.walter?.[key];
      // A dash, not a zero. See above.
      this.rows[key].innerHTML = lb
        ? `<span class="board-form">${key.toUpperCase()}</span>` +
          `<span class="board-weight num">${lb.toFixed(2)} LBS</span>` +
          `<span class="board-tick">&#10003;</span>`
        : `<span class="board-form">${key.toUpperCase()}</span>` +
          `<span class="board-weight dash">——</span><span class="board-tick"></span>`;
      this.sight[key].textContent = String(records.sightings?.[key] ?? 0);
    }

    this.headline.textContent = headline ?? '';
    this.headline.classList.toggle('on', !!headline);

    this.root.classList.add('on');
    this.ui.classList.add('celebrating');
  }

  hide() {
    if (!this.active) return;
    this.active = false;
    this.root.classList.remove('on');
    this.ui.classList.remove('celebrating');
    this.onDone?.();
  }
}
