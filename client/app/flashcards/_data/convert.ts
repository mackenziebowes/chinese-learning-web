import { cwd } from "node:process";
import { join } from "node:path";
import { parse } from "csv/sync";
import { type Record } from "./types";

export function line(content: string, depth: number): string {
  return `\n${"\t".repeat(depth)}${content}`;
}

export class FileBuilder {
  private lines: string[] = [];

  addLine(content: string, depth: number = 0): void {
    this.lines.push(`${"\t".repeat(depth)}${content}`);
  }

  addEmptyLine(): void {
    this.lines.push("");
  }

  build(): string {
    return this.lines.join("\n");
  }
}

async function main() {
  const csvContents = await Bun.file(
    join(cwd(), "/app/flashcards/_data/learned_words.csv"),
  ).text();

  const records = parse(csvContents, {
    columns: true,
    skip_empty_lines: true,
  }) as unknown as Record[];

  const fb = new FileBuilder();

  fb.addLine(`export const LEARNED_WORDS = [`);
  records.forEach((record) => {
    fb.addLine(`{`, 1);
    fb.addLine(`chinese: "${record.chinese}",`, 2);
    fb.addLine(`pinyin: "${record.pinyin}",`, 2);
    fb.addLine(`english: "${record.english}",`, 2);
    fb.addLine(`},`, 1);
  });
  fb.addLine(`];`);

  const out = fb.build();
  await Bun.write(join(cwd(), "/app/flashcards/_data/learned_words.ts"), out);
}

main();
