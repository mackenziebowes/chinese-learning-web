import { useRouter } from "./lib/routes";
import App from "./routes";
import Flashcard from "./routes/flashcard";
export default function MainApp() {
  const route = useRouter((s) => s.route);
  switch (route) {
    case "/":
      return <App />;
    case "/flashcards":
      return <Flashcard />;
  }
}
