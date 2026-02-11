import "@/index.css";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default function Flashcard() {
  return (
    <div className="min-h-screen bg-linear-to-br from-slate-50 to-slate-100 flex flex-col items-center justify-center p-8">
      <div className="w-full max-w-2xl space-y-8">
        <h3>Flashcards</h3>
      </div>
    </div>
  );
}
