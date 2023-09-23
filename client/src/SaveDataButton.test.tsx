import { render, screen } from "@testing-library/react";
import SaveDataButton from "./SaveDataButton";

test("renders SaveDataButton", () => {
  render(<SaveDataButton onClickAction={() => {}} />);
  const buttonElement = screen.getByRole("button");
  expect(buttonElement).toBeInTheDocument();
});
