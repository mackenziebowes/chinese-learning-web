"use client";

import { useState } from "react";

import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
// import { Field } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import { type Record } from "../_data/types";

type IncrementRecord = () => void;

export default function Flashcard(args: {
  record: Record;
  increment: IncrementRecord;
  idx: number;
}) {
  const [shouldShowHint, set_shouldShowHint] = useState<boolean>(false);
  const [guess, set_guess] = useState<string>("");
  const [canProgress, set_canProgress] = useState<boolean>(false);

  const handleGuess = () => {
    if (guess == args.record.english) set_canProgress(true);
  };

  const increment = () => {
    args.increment();
    set_shouldShowHint(false);
    set_canProgress(false);
  };

  return (
    <Card>
      <CardHeader>
        <h3>Question {args.idx}</h3>
      </CardHeader>
      <CardContent className="flex flex-col gap-2">
        <p className="text-4xl">{args.record.chinese}</p>
        {shouldShowHint && <p className="text-2xl">{args.record.pinyin}</p>}
        <Button variant="outline" onClick={() => set_shouldShowHint((v) => !v)}>
          {shouldShowHint ? "Hide Hint" : "Show Hint"}
        </Button>
        <Input
          type="text"
          value={guess}
          onChange={(e) => set_guess(e.target.value)}
          placeholder="Guess"
        />
        <Button variant="outline" onClick={() => handleGuess()}>
          Guess
        </Button>
        {canProgress && (
          <>
            <Button variant="outline" onClick={() => increment()}>
              Go Next
            </Button>
          </>
        )}
      </CardContent>
    </Card>
  );
}
