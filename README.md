# 🚗 Détection et Tracking d'Objets avec YOLO

Petit projet de Computer Vision : détecter des personnes dans une vidéo, les suivre d'une frame à l'autre, et compter celles qui franchissent une ligne — avec YOLOv8 et OpenCV.

## Le problème

Je voulais découvrir concrètement si le Computer Vision (détection d'objets / analyse vidéo) est un domaine qui m'intéresse vraiment, en construisant un petit projet que je vais réellement terminer — pas un énième projet commencé puis abandonné.

## La solution

Un pipeline complet qui part d'une vidéo brute et produit une vidéo annotée : détection des personnes avec YOLOv8, tracking pour leur donner un ID stable dans le temps, et une fonctionnalité de comptage des personnes qui franchissent une ligne virtuelle.

## Technologies utilisées

- **Python 3**
- **OpenCV** (`opencv-python`) — lecture/écriture vidéo frame par frame, dessin des annotations (boîtes, ligne, compteur)
- **Ultralytics YOLOv8** (`yolov8n`, pré-entraîné sur COCO, 80 classes) — détection d'objets et tracking multi-objets intégré (ByteTrack)
- **Git / GitHub**

## Pipeline

```
Vidéo (vtest.avi)
        │
        ▼
Lecture frame par frame (OpenCV)
        │
        ▼
Détection d'objets (YOLOv8n)
        │
        ▼
Tracking multi-objets (ByteTrack, via model.track())
        │
        ▼
ID stable par personne + ligne de comptage
        │
        ▼
Vidéo annotée en sortie (boîtes, IDs, compteur)
```

Le projet a été construit étape par étape, chaque script ajoutant une brique au pipeline :

| Script | Rôle |
|---|---|
| `explore_video.py` | Lecture d'une vidéo, métadonnées (FPS, dimensions, frames) |
| `yolo_test.py` | Première détection YOLO sur une image, inspection du résultat brut |
| `detect_video.py` | Détection YOLO sur la vidéo complète |
| `track_video.py` | Ajout du tracking (ID stable par personne) |
| `count_line.py` | Ajout de la ligne de comptage (fonctionnalité finale) |

## Comment lancer le projet

```bash
git clone <url-du-repo>
cd object-tracking-yolo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 count_line.py
```

La vidéo annotée est générée dans `data/output_line.mp4`.

## Exemple de résultat

![Détection, tracking et comptage sur une frame de la vidéo](example_output.jpg)

## Limites

- **Modèle nano** (le plus léger/rapide de YOLOv8) : quelques faux positifs possibles sur des objets fixes du décor (confondus avec un objet mobile à faible confidence).
- **ID switch** : quand deux personnes se croisent ou que l'une est temporairement cachée, le tracker peut lui attribuer un nouvel ID à sa réapparition — limite connue des trackers basés sur la position plutôt que sur l'apparence.
- **Ligne de comptage horizontale à hauteur fixe** : à cause de la perspective de la caméra, les personnes qui arrivent par les côtés de l'image peuvent traverser la zone sans être comptées. Une ligne suivant l'angle réel du chemin serait plus précise, mais dépasse le périmètre choisi pour ce projet.
- Traitement de la vidéo en différé (pas en temps réel).

## Ce que j'ai appris

*(à compléter avec mes propres mots avant publication)*

## Remerciements

Vidéo de test `vtest.avi` fournie par le dépôt officiel OpenCV (samples).
