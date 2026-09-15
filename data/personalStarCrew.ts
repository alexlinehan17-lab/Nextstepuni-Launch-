import type { StarCrewArtwork } from "./starCrewTypes";

/** Stable profile IDs; existing DiceBear seeds remain valid. */
export const PERSONAL_STAR_CREW: (StarCrewArtwork & { id: string; name: string })[] = [
  {
    "id": "star-crew:beanie",
    "name": "The Beanie",
    "src": "/assets/star-crew/personal/original-four.png",
    "frame": {
      "width": 94.7791,
      "left": -4.19186,
      "top": -0.488372,
      "tile": 0
    }
  },
  {
    "id": "star-crew:reader",
    "name": "The Reader",
    "src": "/assets/star-crew/personal/original-four.png",
    "frame": {
      "width": 101.8875,
      "left": 1.16875,
      "top": -6.55,
      "tile": 1
    }
  },
  {
    "id": "star-crew:skater",
    "name": "The Skater",
    "src": "/assets/star-crew/personal/05-skater.png",
    "frame": {
      "width": 109.2872,
      "left": -4.643575,
      "top": -3.031285
    }
  },
  {
    "id": "star-crew:maker",
    "name": "The Maker",
    "src": "/assets/star-crew/personal/07-maker.png",
    "frame": {
      "width": 109.2872,
      "left": -5.07933,
      "top": -3.205587
    }
  },
  {
    "id": "star-crew:stargazer",
    "name": "The Stargazer",
    "src": "/assets/star-crew/personal/08-stargazer.png",
    "frame": {
      "width": 110.898,
      "left": -5.846939,
      "top": -3.238095
    }
  },
  {
    "id": "star-crew:hugger",
    "name": "The Hugger",
    "src": "/assets/star-crew/personal/09-hugger.png",
    "frame": {
      "width": 103.0685,
      "left": -0.219178,
      "top": -1.493151
    }
  },
  {
    "id": "star-crew:snoozer",
    "name": "The Snoozer",
    "src": "/assets/star-crew/personal/11-snoozer.png",
    "frame": {
      "width": 125.561,
      "left": -13.130937,
      "top": -12.830552
    }
  },
  {
    "id": "star-crew:musician",
    "name": "The Musician",
    "src": "/assets/star-crew/personal/12-musician.png",
    "frame": {
      "width": 105.0612,
      "left": -2.530612,
      "top": -1.39957
    }
  }
];

export const getPersonalStarCrew = (id: string) => PERSONAL_STAR_CREW.find(avatar => avatar.id === id);
export const getAvatarName = (id: string) => getPersonalStarCrew(id)?.name ?? id;
