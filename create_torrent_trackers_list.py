import asyncio
import re
import aiohttp

# ----------------------------------------------------------------------
# Helper: fetch raw file content from a GitHub URL
# ----------------------------------------------------------------------
async def fetch_github_raw(url: str, session: aiohttp.ClientSession) -> str:
    """
    Convert a normal GitHub file URL to its raw counterpart and download it.
    """
    # Example: https://github.com/user/repo/blob/main/file.txt
    raw_url = re.sub(
        r"https?://github\.com/(.+?)/blob/(.+)",
        r"https://raw.githubusercontent.com/\1/\2",
        url,
    )
    async with session.get(raw_url) as resp:
        resp.raise_for_status()
        return await resp.text()

# ----------------------------------------------------------------------
# Main: combine tracker lists from multiple GitHub URLs
# ----------------------------------------------------------------------
async def combine_tracker_lists(urls):
    """
    Download each tracker list, deduplicate entries and return a single string.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_github_raw(u, session) for u in urls]
        raw_contents = await asyncio.gather(*tasks, return_exceptions=True)

    trackers = set()
    for content in raw_contents:
        if isinstance(content, Exception):
            # Skip failed downloads but keep the error visible for debugging
            print(f"⚠️  Failed to fetch a list: {content}")
            continue

        for line in content.splitlines():
            line = line.strip()
            # Ignore empty lines and comments (common in tracker files)
            if line and not line.startswith("#"):
                trackers.add(line)

    # Return a nicely formatted list (one tracker per line)
    return "\n".join(sorted(trackers))

def double_space_trackers(tracker_list):
    """
    Return a single string where each tracker URL is separated by a
    blank line.  Empty or comment lines in the input are ignored.
    """
    # Clean the input - strip whitespace and drop blanks/comments
    clean = [t.strip() for t in tracker_list if t.strip() and not t.strip().startswith('#')]

    # Join with two newline characters (one for the line break,
    # one for the blank line)
    return "\n\n".join(clean) + "\n"   # final newline is optional

if __name__ == "__main__":
    github_urls = [
        "https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_best.txt",
        "https://raw.githubusercontent.com/XIU2/TrackersListCollection/master/best.txt"
    ]

    combined = asyncio.run(combine_tracker_lists(github_urls))
    #print(combined)

    CUSTOM_LINES = """\
    http://plab.site/ann?uk=3ZA1fbbgjL
    http://plab.site/ann?uk=0EQxNEINP3
    http://plab.site/ann?uk=0EQxNEINP3
    http://plab.site/ann?uk=1G3Up69e1x
    http://plab.site/ann?uk=1G3Up69e1x
    http://plab.site/ann?uk=3y4LvfjV4s
    http://plab.site/ann?uk=3y4LvfjV4s
    http://plab.site/ann?uk=410G4OwtVb
    http://plab.site/ann?uk=410G4OwtVb
    http://plab.site/ann?uk=AsAXNzsr4V
    http://plab.site/ann?uk=AsAXNzsr4V
    http://plab.site/ann?uk=G7NRnIhAtl
    http://plab.site/ann?uk=G7NRnIhAtl
    http://plab.site/ann?uk=L989SlNLo8
    http://plab.site/ann?uk=L989SlNLo8
    http://plab.site/ann?uk=N0nrwjNNgu
    http://plab.site/ann?uk=N0nrwjNNgu
    http://plab.site/ann?uk=T0YQIDjHY1
    http://plab.site/ann?uk=T0YQIDjHY1
    http://plab.site/ann?uk=ZA9LuUCu2P
    http://plab.site/ann?uk=ZA9LuUCu2P
    http://plab.site/ann?uk=dE6NPsVsqy
    http://plab.site/ann?uk=dE6NPsVsqy
    http://plab.site/ann?uk=xnqfz3H1FE
    http://plab.site/ann?uk=xnqfz3H1FE

    udp://tracker.opentrackr.org:1337/announce

    udp://explodie.org:6969/announce

    udp://open.stealth.si:80/announce

    http://tracker.bt4g.com:2095/announce

    udp://z.mercax.com:53/announce

    https://tracker.tamersunion.org:443/announce

    https://tracker.lilithraws.org:443/announce

    https://www.peckservers.com:9443/announce

    https://trackers.mlsub.net:443/announce

    https://tracker.yemekyedim.com:443/announce

    udp://amigacity.xyz:6969/announce

    https://tracker.gcrenwp.top:443/announce

    udp://trackarr.org:6969/announce

    udp://tr4ck3r.duckdns.org:6969/announce

    https://tr.zukizuki.org:443/announce

    https://tracker.moeking.me:443/announce

    http://tk.leechshield.link:80/announce

    udp://exodus.desync.com:6969/announce

    udp://tracker.breizh.pm:6969/announce

    udp://open.demonii.com:1337/announce

    udp://ttk2.nbaonlineservice.com:6969/announce

    udp://odd-hd.fr:6969/announce

    udp://evan.im:6969/announce

    udp://tracker.deadorbit.nl:6969/announce

    udp://tracker.dler.com:6969/announce

    udp://tracker.torrent.eu.org:451/announce

    udp://ns1.monolithindustries.com:6969/announce

    udp://martin-gebhardt.eu:25/announce

    https://tracker.leechshield.link:443/announce

    http://tracker.vraphim.com:6969/announce

    udp://tracker.fnix.net:6969/announce

    udp://seedpeer.net:6969/announce

    udp://bandito.byterunner.io:6969/announce

    udp://serpb.vpsburti.com:6969/announce

    udp://tracker.srv00.com:6969/announce

    udp://run.publictracker.xyz:6969/announce

    http://public.tracker.vraphim.com:6969/announce

    http://bt.okmp3.ru:2710/announce

    udp://open.dstud.io:6969/announce

    udp://tracker.tryhackx.org:6969/announce

    http://tracker-zhuqiy.dgj055.icu:80/announce

    udp://ismaarino.com:1234/announce

    udp://tracker.gigantino.net:6969/announce

    http://tracker1.itzmx.com:8080/announce

    udp://ec2-18-191-163-220.us-east-2.compute.amazonaws.com:6969/announce

    udp://tracker.gmi.gd:6969/announce

    udp://tracker.0x7c0.com:6969/announce

    udp://p2p.publictracker.xyz:6969/announce

    udp://tracker.filemail.com:6969/announce

    udp://t.overflow.biz:6969/announce

    udp://tracker.qu.ax:6969/announce

    https://sparkle.ghostchu-services.top:443/announce

    http://bvarf.tracker.sh:2086/announce

    http://saltwood.top:6969/announce

    udp://u4.trakx.crim.ist:1337/announce

    udp://d40969.acod.regrucolo.ru:6969/announce

    http://kiryuu-test.mywaifu.best:6969/announce

    https://tracker.cloudit.top:443/announce

    udp://opentracker.io:6969/announce

    http://tracker.renfei.net:8080/announce

    udp://www.torrent.eu.org:451/announce

    udp://tk4.leechshield.link:6969/announce

    udp://retracker.lanta.me:2710/announce

    https://api.ipv4online.uk:443/announce

    https://tracker.bjut.jp:443/announce

    udp://tracker-udp.gbitt.info:80/announce

    udp://tk1.trackerservers.com:8080/announce

    udp://bittorrent-tracker.e-n-c-r-y-p-t.net:1337/announce

    https://mathkangaroo.jp:443/announce

    http://ipv4announce.sktorrent.eu:6969/announce
    """

    combined = combined + CUSTOM_LINES
    combined = double_space_trackers(combined)

    # Write the combined list to a file
    with open("torrent_trackers_combined_list.txt", "w", encoding="utf-8") as f:
        f.write(combined)
