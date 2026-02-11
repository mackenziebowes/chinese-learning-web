import { create } from "zustand";

export type ValidRoutes = "/" | "/flashcards";

interface RouterState {
  route: ValidRoutes;
  setRoute: (newRoute: ValidRoutes) => void;
}

export const useRouter = create<RouterState>((set) => ({
  route: "/",
  setRoute: (newRoute: ValidRoutes) => set((state) => ({ route: newRoute })),
}));
