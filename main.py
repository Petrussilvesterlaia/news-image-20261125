"""Titik masuk entri poster berita dunia 25 November 2026.

Program ini merender poster 1024x1024 lewat fungsi render dari modul
draw, lalu menulis hasilnya ke path yang diminta.

Path keluaran diambil dari variabel lingkungan ENTRY_OUTPUT; bila tidak
ada, dipakai /output/entry.png. Program ini tidak pernah menulis apa pun
ke dalam direktori skripnya sendiri — satu-satunya berkas yang dibuat
adalah PNG hasil render di path keluaran.
"""

import os
import sys


def _direktori_skrip():
    """Direktori tempat berkas ini berada, apa pun direktori kerjanya."""
    return os.path.dirname(os.path.abspath(__file__))


def main():
    # Pastikan modul draw (satu direktori dengan berkas ini) bisa diimpor
    # walau interpreter dijalankan dengan -P, yang tidak menambahkan
    # direktori skrip ke sys.path secara otomatis.
    direktori = _direktori_skrip()
    if direktori not in sys.path:
        sys.path.insert(0, direktori)

    from draw import render

    keluaran = os.environ.get("ENTRY_OUTPUT") or "/output/entry.png"
    induk = os.path.dirname(os.path.abspath(keluaran))
    if induk:
        os.makedirs(induk, exist_ok=True)

    render(keluaran)

    ukuran = os.path.getsize(keluaran)
    print(f"Wrote {keluaran} ({ukuran} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
