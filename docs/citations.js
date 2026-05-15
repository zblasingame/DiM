/* ───────────────────────────────────────────────────────────────────
   citations.js — resolves <span class="cite" data-key="…"></span>
   into numbered author-year citations + an auto-built References
   section with back-references.

   Ported from zblasingame.github.io / assets/js/citations.js, trimmed
   to the keys referenced on this page (DiM landing page).
   ─────────────────────────────────────────────────────────────────── */
(function(){
  const C = {
    // ─── face morphing / FR ───
    'ferrara_magicpassport':{authors:'Ferrara, M., Franco, A., Maltoni, D.', title:'The magic passport', venue:'IJCB', year:2014},
    'mipgan':            {authors:'Zhang, H., Venkatesh, S., Ramachandra, R., Raja, K., Damer, N., Busch, C.', title:'MIPGAN — Generating Strong and High Quality Morphing Attacks Using Identity Prior Driven GAN', venue:'IEEE T-BIOM 3(3)', year:2021, url:'https://arxiv.org/abs/2009.01729'},
    'mmpmr':             {authors:'Scherhag, U., Nautsch, A., Rathgeb, C., et al.', title:'Biometric Systems under Morphing Attacks: Assessment of Morphing Techniques and Vulnerability Reporting', venue:'BIOSIG', year:2017},
    'arcface':           {authors:'Deng, J., Guo, J., Xue, N., Zafeiriou, S.', title:'ArcFace: Additive Angular Margin Loss for Deep Face Recognition', venue:'CVPR', year:2019, url:'https://arxiv.org/abs/1801.07698'},
    'blasingame_dim':    {authors:'Blasingame, Z. W., Liu, C.', title:'Leveraging Diffusion for Strong and High Quality Face Morphing Attacks', venue:'IEEE T-BIOM 6(1)', year:2024, doi:'10.1109/TBIOM.2024.3349857'},
    'fast_dim':          {authors:'Blasingame, Z. W., Liu, C.', title:'Fast-DiM: Towards Fast Diffusion Morphs', venue:'IEEE Security &amp; Privacy 22(4)', year:2024, doi:'10.1109/MSEC.2024.3410112'},

    // ─── GAN / inversion ───
    'stylegan2':         {authors:'Karras, T., Laine, S., Aittala, M., Hellsten, J., Lehtinen, J., Aila, T.', title:'Analyzing and Improving the Image Quality of StyleGAN', venue:'CVPR', year:2020, url:'https://arxiv.org/abs/1912.04958'},
    'e4e':               {authors:'Tov, O., Alaluf, Y., Nitzan, Y., Patashnik, O., Cohen-Or, D.', title:'Designing an Encoder for StyleGAN Image Manipulation', venue:'ACM TOG 40(4) (SIGGRAPH)', year:2021, url:'https://arxiv.org/abs/2102.02766'},

    // ─── diffusion / generative ───
    'ddpm':              {authors:'Ho, J., Jain, A., Abbeel, P.', title:'Denoising Diffusion Probabilistic Models', venue:'NeurIPS', year:2020, url:'https://arxiv.org/abs/2006.11239'},
    'song2021scorebased':{authors:'Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S., Poole, B.', title:'Score-Based Generative Modeling through Stochastic Differential Equations', venue:'ICLR', year:2021, url:'https://arxiv.org/abs/2011.13456'},
    'song2021denoising': {authors:'Song, J., Meng, C., Ermon, S.', title:'Denoising Diffusion Implicit Models', venue:'ICLR', year:2021, url:'https://arxiv.org/abs/2010.02502'},
    'diff_beat_gan':     {authors:'Dhariwal, P., Nichol, A.', title:'Diffusion Models Beat GANs on Image Synthesis', venue:'NeurIPS', year:2021, url:'https://arxiv.org/abs/2105.05233'},
    'diffae':            {authors:'Preechakul, K., Chatthee, N., Wizadwongsa, S., Suwajanakorn, S.', title:'Diffusion Autoencoders: Toward a Meaningful and Decodable Representation', venue:'CVPR', year:2022, url:'https://arxiv.org/abs/2111.15640'},

    // ─── solvers ───
    'lu2023dpmsolver':   {authors:'Lu, C., Zhou, Y., Bao, F., Chen, J., Li, C., Zhu, J.', title:'DPM-Solver++: Fast Solver for Guided Sampling of Diffusion Probabilistic Models', venue:'arXiv:2211.01095', year:2022, url:'https://arxiv.org/abs/2211.01095'},

    // ─── eval ───
    'fid_heusel':        {authors:'Heusel, M., Ramsauer, H., Unterthiner, T., Nessler, B., Hochreiter, S.', title:'GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium', venue:'NeurIPS', year:2017, url:'https://arxiv.org/abs/1706.08500'},

    // Rex
    'blasingame2026rex': {authors:'Blasingame, Z. W., Liu, C.', title:'Rex: A Family of Reversible Exponential (Stochastic) Runge-Kutta Solvers', venue:'ICML', year:2026, url:'https://arxiv.org/abs/2502.08834'},
  };

  /* ─── Sidenote (footnote) markup ─────────────────────────────── */
  let snCounter = 0;
  function makeNote(html){
    snCounter += 1;
    const id = 'sn-' + snCounter;
    const sup  = '<label class="margin-toggle-label" for="' + id + '"><sup class="sidenote-number"></sup></label>';
    const cb   = '<input type="checkbox" id="' + id + '" class="margin-toggle">';
    const note = '<span class="sidenote">' + html + '</span>';
    return sup + cb + note;
  }

  /* ─── Author-year formatting helpers ─────────────────────────── */
  function parseSurnames(s){
    if(!s) return [];
    const parts = s.split(',').map(t => t.trim()).filter(Boolean);
    const out = [];
    for(const p of parts){
      if(/^et\s+al\.?$/i.test(p)) { out.push('et al.'); continue; }
      if(/^([A-Z]\.?\s*\-?\s*)+$/.test(p)) continue;
      out.push(p);
    }
    return out;
  }
  function shortAuthors(s){
    const sur = parseSurnames(s);
    if(!sur.length) return '';
    if(sur.length === 1) return sur[0];
    if(sur[1] === 'et al.') return sur[0] + ' et al.';
    if(sur.length === 2)   return sur[0] + ' and ' + sur[1];
    return sur[0] + ' et al.';
  }

  /* ─── Bibliography entry formatting ──────────────────────────── */
  function fmtBibEntry(key){
    const c = C[key];
    if(!c) return '<em>[missing: ' + key + ']</em>';
    let s = '';
    if(c.authors) s += c.authors;
    if(c.year)    s += ' (' + c.year + ').';
    if(c.title){
      s += ' <em>' + c.title + '</em>';
      if(!/[.!?]$/.test(c.title)) s += '.';
    }
    if(c.venue) s += ' ' + c.venue + '.';
    if(c.url)       s += ' <a href="' + c.url + '">link</a>';
    else if(c.doi)  s += ' <a href="https://doi.org/' + c.doi + '">doi</a>';
    return s;
  }

  /* ─── Main pass ──────────────────────────────────────────────── */
  function process(){
    const cited = Object.create(null);
    let siteCounter = 0;

    document.querySelectorAll('.cite').forEach(el => {
      const keys = (el.getAttribute('data-key') || '').split(',').map(s => s.trim()).filter(Boolean);
      if(!keys.length){ el.remove(); return; }
      const style = (el.getAttribute('data-style') || 'parenthetical').toLowerCase();

      siteCounter += 1;
      const siteId = 'cite-' + siteCounter;

      const parts = keys.map(k => {
        const c = C[k];
        if(!c){
          return '<span class="cite-missing">[missing: ' + k + ']</span>';
        }
        (cited[k] = cited[k] || []).push({id: siteId, idx: siteCounter});
        const auth = shortAuthors(c.authors);
        const year = c.year || 'n.d.';
        const href = '#bib-' + cssEscape(k);
        if(style === 'year' && keys.length === 1){
          return '<a href="' + href + '" class="cite-link">(' + year + ')</a>';
        }
        if(style === 'narrative' && keys.length === 1){
          return '<a href="' + href + '" class="cite-link">' + auth + '</a>\u202F(' + year + ')';
        }
        return '<a href="' + href + '" class="cite-link">' + auth + ', ' + year + '</a>';
      });

      let inner;
      if((style === 'narrative' || style === 'year') && keys.length === 1){
        inner = parts[0];
      } else {
        inner = '(' + parts.join('; ') + ')';
      }
      const html = '<span class="cite-inline" id="' + siteId + '">' + inner + '</span>';

      const tmp = document.createElement('span');
      tmp.innerHTML = html;
      const node = tmp.firstChild;

      const prev = el.previousSibling;
      const needSpace = prev && prev.nodeType === Node.TEXT_NODE && !/\s$/.test(prev.nodeValue)
                      || prev && prev.nodeType === Node.ELEMENT_NODE;
      el.replaceWith(node);
      if(needSpace){
        node.parentNode.insertBefore(document.createTextNode(' '), node);
      }
    });

    document.querySelectorAll('.footnote').forEach(el => {
      const html = el.innerHTML;
      const wrap = document.createElement('span');
      wrap.innerHTML = makeNote(html);
      el.replaceWith(wrap);
    });

    document.querySelectorAll('.margin').forEach(el => {
      el.classList.remove('margin');
      el.classList.add('marginnote');
    });

    buildBibliography(cited);
  }

  function buildBibliography(cited){
    const keys = Object.keys(cited);
    if(!keys.length) return;

    keys.sort((a, b) => {
      const A = (parseSurnames((C[a]||{}).authors)[0] || a).toLowerCase();
      const B = (parseSurnames((C[b]||{}).authors)[0] || b).toLowerCase();
      if(A < B) return -1;
      if(A > B) return  1;
      const yA = (C[a]||{}).year || 0;
      const yB = (C[b]||{}).year || 0;
      return yA - yB;
    });

    // Target container — inside #references if it exists, else appended to body
    let host = document.getElementById('references-list-host');
    if(!host){
      const section = document.createElement('section');
      section.id = 'references';
      section.className = 'references';
      section.setAttribute('aria-label', 'References');
      const wrap = document.createElement('div');
      wrap.className = 'article-wrapper';
      const h2 = document.createElement('h2');
      h2.textContent = 'References';
      wrap.appendChild(h2);
      host = document.createElement('div');
      host.id = 'references-list-host';
      wrap.appendChild(host);
      section.appendChild(wrap);
      document.body.appendChild(section);
    }

    const ol = document.createElement('ol');
    ol.className = 'bib-list';

    keys.forEach(k => {
      const li = document.createElement('li');
      li.id = 'bib-' + cssEscape(k);
      li.className = 'bib-entry';

      const body = document.createElement('span');
      body.className = 'bib-body';
      body.innerHTML = fmtBibEntry(k);
      li.appendChild(body);

      const sites = cited[k];
      if(sites && sites.length){
        const back = document.createElement('span');
        back.className = 'bib-backrefs';
        back.appendChild(document.createTextNode(' ['));
        sites.forEach((s, i) => {
          if(i) back.appendChild(document.createTextNode(', '));
          const a = document.createElement('a');
          a.href = '#' + s.id;
          a.className = 'bib-backref';
          a.textContent = '§' + s.idx;
          back.appendChild(a);
        });
        back.appendChild(document.createTextNode(']'));
        li.appendChild(back);
      }

      ol.appendChild(li);
    });
    // Clear any prior content and append
    while(host.firstChild) host.removeChild(host.firstChild);
    host.appendChild(ol);
  }

  function cssEscape(s){
    if(window.CSS && CSS.escape) return CSS.escape(s);
    return String(s).replace(/[^a-zA-Z0-9_\-]/g, '_');
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', process);
  } else {
    process();
  }
})();
