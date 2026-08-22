import { readFile } from "node:fs/promises"
import { dirname, join } from "node:path"
import { fileURLToPath } from "node:url"

const root = join(dirname(fileURLToPath(import.meta.url)), "..", "..", "..")
const skillsPath = join(root, "plugins", "gopher", "skills")
const agentsPath = join(root, "plugins", "gopher", "agents", "opencode")

async function prompt(name) {
  const source = await readFile(join(agentsPath, `${name}.md`), "utf8")
  return source.replace(/^---\n[\s\S]*?\n---\n/, "").trim()
}

function role(name, description, mode, permission, body) {
  return {
    name,
    description,
    mode,
    permission,
    prompt: body,
  }
}

export default {
  id: "@alvadorncorp/gopher",
  server: async () => {
    const [architect, developer, reviewer] = await Promise.all([
      prompt("architect"),
      prompt("developer"),
      prompt("reviewer"),
    ])

    return {
      config(config) {
        config.skills ??= {}
        config.skills.paths ??= []
        if (!config.skills.paths.includes(skillsPath)) config.skills.paths.push(skillsPath)

        config.agent ??= {}
        config.agent["gopher-architect"] = role(
          "gopher-architect",
          "Assesses delegated Go structural changes through the architecture skill without applying unapproved edits.",
          "subagent",
          { edit: "deny", task: "deny", skill: { "*": "deny", architecture: "allow" } },
          architect,
        )
        config.agent["gopher-developer"] = role(
          "gopher-developer",
          "Implements a delegated local, reversible Go change through the developer skill.",
          "subagent",
          { task: "deny", skill: { "*": "deny", developer: "allow" } },
          developer,
        )
        config.agent["gopher-reviewer"] = role(
          "gopher-reviewer",
          "Runs a read-only multi-lens Go review through the review skill and delegates each lens to explore.",
          "primary",
          { edit: "deny", task: { "*": "deny", explore: "allow" }, skill: { "*": "deny", review: "allow" } },
          reviewer,
        )
      },
    }
  },
}
