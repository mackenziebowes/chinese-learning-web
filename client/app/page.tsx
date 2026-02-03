import Link from "next/link";
import { ButtonGroup } from "@/components/ui/button-group";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div className="grid place-items-center w-svh min-h-svh overflow-clip">
      <div className="flex flex-col gap-2">
        <h1 className="text-2xl lg:text-4xl">Learn Chinese</h1>
        <ButtonGroup>
          <Button asChild variant="default">
            <Link href="/flashcards">Flash Cards</Link>
          </Button>
          <Button>
            <Link href="/see-and-say">See and Say</Link>
          </Button>
        </ButtonGroup>
      </div>
    </div>
  );
}
