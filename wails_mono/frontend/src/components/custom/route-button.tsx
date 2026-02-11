import { Button, type ButtonProps } from "../ui/button";
import { useRouter, type ValidRoutes } from "@/lib/routes";
export type RouteButtonProps = ButtonProps & {
  route: ValidRoutes;
};

export function RouteButton({
  route,
  variant,
  size,
  className,
  children,
}: RouteButtonProps) {
  const setRoute = useRouter((s) => s.setRoute);

  return (
    <Button
      size={size}
      variant={variant}
      className={className}
      onClick={() => setRoute(route)}
    >
      {children}
    </Button>
  );
}
