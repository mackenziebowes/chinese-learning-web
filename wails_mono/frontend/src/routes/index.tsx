import { useState } from "react";
import logo from "@/assets/images/logo-universal.png";
import "@/index.css";
import { Greet } from "../../wailsjs/go/main/App";
import { Button } from "@/components/ui/button";
import { RouteButton } from "@/components/custom/route-button";
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
import { useRouter } from "@/lib/routes";

function App() {
  const [resultText, setResultText] = useState(
    "Enter your name to get started!",
  );
  const [name, setName] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function greet() {
    if (!name.trim()) {
      setResultText("Please enter a name first! 🙏");
      return;
    }

    setIsLoading(true);
    try {
      const result = await Greet(name);
      setResultText(result);
    } catch (error) {
      setResultText("Oops! Something went wrong. 😕");
    } finally {
      setIsLoading(false);
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      greet();
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-slate-50 to-slate-100 flex flex-col items-center justify-center p-8">
      <div className="w-full max-w-2xl space-y-8">
        {/* Main Card */}
        <Card className="shadow-xl border-slate-200">
          <CardHeader>
            <CardTitle className="text-2xl">Learn Chinese</CardTitle>
            <CardDescription>
              Learn Chinese with this application!
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <RouteButton route="/flashcards" variant="outline">
              Flashcards
            </RouteButton>
          </CardContent>
          <CardFooter className="flex gap-3">
            <Button asChild>
              <a href="https://github.com/mackenziebowes/chinese-learning-web">
                View on Github
              </a>
            </Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  );
}

export default App;
