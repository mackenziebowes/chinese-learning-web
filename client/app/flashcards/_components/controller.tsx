"use client";

import { useState } from "react";
import { LEARNED_WORDS } from "../_data/learned_words";
import Flashcard from "./flashcard";

export default function FlashcardController() {
  const [currentId, set_currentId] = useState<number>(0);

  const incrementId = () => {
    set_currentId((v) => Math.min(LEARNED_WORDS.length - 1, v + 1));
  };

  return (
    <>
      <Flashcard
        record={LEARNED_WORDS[currentId]!}
        increment={() => incrementId()}
        idx={currentId}
      />
    </>
  );
}
