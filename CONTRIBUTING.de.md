# Mitwirken

*[English](CONTRIBUTING.md) · Deutsch*

Danke für das Interesse an diesem Projekt. Dies ist ein kleines, selbst
gehostetes Hobby-/Portfolio-Projekt; Beiträge sind willkommen, werden aber
bewusst schlank gehalten.

## Lizenz der Beiträge

Dieses Projekt steht unter der **GNU Affero General Public License v3.0**
(AGPL-3.0, siehe [LICENSE](LICENSE)). Mit einem Beitrag erklärst du dich damit
einverstanden, dass dein Beitrag unter derselben Lizenz bereitgestellt wird.

## Sign-off (Developer Certificate of Origin)

Damit die Herkunft des Codes nachvollziehbar bleibt, müssen Beiträge nach dem
[Developer Certificate of Origin](DCO) (DCO 1.1) **mit Sign-off** versehen
sein. Der Sign-off ist eine einfache Erklärung, dass du das Recht hast, den
Code unter der Projektlizenz beizutragen — er überträgt **keine** Rechte an
eine einzelne Person oder Firma (es gibt kein CLA).

Den Sign-off fügst du je Commit mit `-s` hinzu:

    git commit -s -m "Deine Nachricht"

Das hängt eine Zeile wie diese an:

    Signed-off-by: Dein Name <du@example.com>

Verwende deinen echten Namen (oder ein dauerhaftes Pseudonym) und eine
erreichbare E-Mail-Adresse. Mit dem Sign-off bestätigst du die Punkte aus der
Datei [DCO](DCO).

## Praktische Hinweise

- Prüfe jede Plugin-Änderung auf einer Checkmk-Site mit `cmk-validate-plugins`,
  bevor du sie einreichst — das ist der maßgebliche Test, ob die Plugin-APIs
  zufrieden sind.
- Die mitgelieferten Schwellen und Defaults (SNR-Margin, Fehlerraten,
  `DB_SCALE`) sind bewusst konservative Platzhalter. Pull Requests, die diese
  für eine bestimmte Leitung umjustieren, werden eher nicht übernommen — das
  stellt jeder gegen seine eigene Baseline ein. Verbesserungen am
  *Mechanismus* (neue Metriken, besseres Rate-Handling, zusätzliche
  TR-064-Werte) sind willkommen.
- Das Plugin nutzt die moderne Checkmk-Plugin-API (`cmk_addons`, 2.3+). Bitte
  halte Änderungen zu diesem Layout kompatibel und meide die Legacy-API.
- Halte Änderungen fokussiert und erkläre das „Warum" in der Commit-Nachricht.
- Für größere Änderungen ist es willkommen, vorher ein Issue zu eröffnen.

Keine Zusagen zur Review-Geschwindigkeit — dies ist ein Freizeitprojekt.
