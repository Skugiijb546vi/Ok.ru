name: Video_Stream_Fix
on:
  workflow_dispatch:
    inputs:
      video_url:
        description: 'Direct Link (Seedr)'
        required: true

jobs:
  convert:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: 🏗️ Setup
        run: sudo apt-get update && sudo apt-get install -y aria2 ffmpeg

      - name: ⬇️ Download
        run: |
          aria2c --max-connection-per-server=16 --split=16 -o "source_video" "${{ github.event.inputs.video_url }}"

      - name: 🎬 Process (Universal Format)
        run: |
          ffmpeg -i "source_video" -c:v libx264 -preset veryfast -crf 23 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 128k -y "final_video.mp4"

      - name: 🚀 Upload to Release
        uses: softprops/action-gh-release@v1
        with:
          tag_name: "v${{ github.run_number }}"
          files: final_video.mp4
          body: |
            Direct Link: https://github.com/${{ github.repository }}/releases/download/v${{ github.run_number }}/final_video.mp4
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}