module.exports.readVersion = (contents) => {
  const lines = contents.split(/\r\n|\r|\n/g);

  let versionLine = null;
  for (const line of lines) {
    if (line.includes("version = ")) {
      versionLine = line;
      break;
    }
  }

  if (!(versionLine === null)) {
    const regexp = /(?<=")[^"]*(?=")/;
    return versionLine.match(regexp)[0];
  }
};

module.exports.writeVersion = (contents, version) => {
  const isCRLF = /\r\n/.test(contents);
  const lines = contents.split(/\r\n|\r|\n/g);

  let index = null;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    if (line.includes("version = ")) {
      index = i;
    }
  }

  if (!(index === null)) {
    lines.splice(index, 1, `version = "${version}"`);
  }

  if (isCRLF) {
    return lines.join("\r\n");
  }

  return lines.join("\n");
};
