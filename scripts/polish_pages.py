#!/usr/bin/env python3
"""Systematically fix all 6 investor pages with robust error handling in JS."""
import os, re

TEMPLATES = '/app/web_app/templates'

pages = {}

# ============================== EVOLUTION ==============================
pages['evolution.html'] = {
    'marker': 'loadEvolutionData',
    'js': '''<script>
(function() {
  var chartDom = document.getElementById('growth-chart');
  if (!chartDom) return;
  var chart = echarts.init(chartDom);
  var loader = document.getElementById('timeline');
  if (loader) loader.innerHTML = '<p class="muted">Loading evolution data...</p>';

  fetch('/api/evolution/data')
    .then(function(r) { return r.json(); })
    .then(function(data) {
      var snaps = data.snapshots || [];
      if (snaps.length === 0) {
        document.getElementById('timeline').innerHTML = '<p class="muted">No snapshots yet. The system will auto-generate them weekly.</p>';
        return;
      }
      var latest = snaps[snaps.length - 1];
      document.getElementById('m-nodes').textContent = latest.node_count || '--';
      document.getElementById('m-rels').textContent = latest.relation_count || '--';
      document.getElementById('m-growth').textContent = '+' + (latest.new_relations_count || 0);
      document.getElementById('m-weeks').textContent = snaps.length;

      chart.setOption({
        tooltip: { trigger: 'axis' },
        legend: { data: ['Nodes','Relations'], textStyle: { color: '#1b2430' } },
        xAxis: { type: 'category', data: snaps.map(function(s){return s.week_label}) },
        yAxis: [
          { type: 'value', name: 'Nodes' },
          { type: 'value', name: 'Relations' }
        ],
        series: [
          { name: 'Nodes', type: 'line', smooth: true, data: snaps.map(function(s){return s.node_count}),
            lineStyle: { width: 3, color: '#4a67ff' }, areaStyle: { color: 'rgba(74,103,255,0.1)' } },
          { name: 'Relations', type: 'line', smooth: true, yAxisIndex: 1, data: snaps.map(function(s){return s.relation_count}),
            lineStyle: { width: 3, color: '#18a999' }, areaStyle: { color: 'rgba(24,169,153,0.1)' } }
        ],
        grid: { left: 60, right: 60, top: 40, bottom: 40 }
      });

      var tl = '';
      snaps.slice().reverse().forEach(function(s) {
        var top = typeof s.top_growing_nodes === 'string' ? JSON.parse(s.top_growing_nodes||'[]') : (s.top_growing_nodes||[]);
        var tags = top.slice(0,4).map(function(n){return '<span class="tag auto-tag">'+n.name+'</span>'}).join('');
        tl += '<div class="tl-item"><div class="tl-week">'+s.week_label+'</div>';
        tl += '<div class="tl-body"><h4>'+s.node_count+' nodes, '+s.relation_count+' relations</h4>';
        tl += '<p>+'+ (s.new_relations_count||0) +' new connections</p>';
        if(tags) tl += '<div class="tag-row">'+tags+'</div>';
        tl += '</div></div>';
      });
      document.getElementById('timeline').innerHTML = tl;
    })
    .catch(function(e) {
      document.getElementById('timeline').innerHTML = '<p class="muted">Failed to load: '+e.message+'</p>';
    });
  window.addEventListener('resize', function(){ chart.resize(); });
})();</script>'''
}

# ============================== DASHBOARD ==============================
pages['dashboard.html'] = {
    'marker': 'loadDashboard',
    'js': '''<script src="/static/js/auth.js"></script>
  <script>
(async function() {
  function sv(id,v){var e=document.getElementById(id);if(e)e.textContent=v;}
  try{
    var r=await fetch('/api/dashboard');
    if(!r.ok)throw new Error('HTTP '+r.status);
    var d=await r.json();
    if(d.code==='UNAUTHORIZED'){window.location.href='/login';return;}
    var h=(d.queries_total||0)*0.25, val=Math.round(h*500);
    sv('kpi-hours',Math.round(h)); sv('kpi-value','\\u00a5'+val.toLocaleString());
    sv('kpi-queries',d.queries_total||0); sv('kpi-users',d.user_count||0);
    sv('nar-hours',Math.round(h)); sv('nar-value','\\u00a5'+val.toLocaleString());
    sv('nar-users',d.user_count); sv('nar-queries',d.queries_total);
    sv('nar-nodes',d.node_count||'--'); sv('nar-rels',d.relation_count||'--');

    var w=(d.weekly_activity||[]).map(function(a){return a.week});
    var qs=(d.weekly_activity||[]).map(function(a){return a.queries||0});
    var us=(d.weekly_activity||[]).map(function(a){return a.users||0});

    var c1=echarts.init(document.getElementById('chart-growth'));
    c1.setOption({title:{text:'User Growth',textStyle:{fontSize:14}},xAxis:{type:'category',data:w},yAxis:{type:'value'},
      series:[{name:'Users',type:'bar',data:us,itemStyle:{color:'#4a67ff',borderRadius:[6,6,0,0]}}],
      grid:{left:50,right:20,top:40,bottom:30}});

    var c2=echarts.init(document.getElementById('chart-activity'));
    c2.setOption({title:{text:'Weekly Queries',textStyle:{fontSize:14}},xAxis:{type:'category',data:w},yAxis:{type:'value'},
      series:[{name:'Queries',type:'line',smooth:true,data:qs,lineStyle:{width:3,color:'#18a999'},
      itemStyle:{color:'#18a999'},areaStyle:{color:'rgba(24,169,153,0.1)'}}],
      grid:{left:50,right:20,top:40,bottom:30}});
    window.addEventListener('resize',function(){c1.resize();c2.resize();});
  }catch(e){sv('kpi-hours','ERR');sv('kpi-value','ERR');}
})();</script>'''
}

# ============================== SIGNALS ==============================
pages['signals.html'] = {
    'marker': 'loadSignals',
    'js': '''<script src="/static/js/auth.js"></script>
  <script>
(async function(){
  function el(id){return document.getElementById(id);}
  try{
    var sr=await fetch('/api/signals');
    if(!sr.ok)throw new Error('HTTP '+sr.status);
    var sd=await sr.json();
    if(sd.code==='UNAUTHORIZED'){window.location.href='/login';return;}
    var sigs=sd.signals||[];

    var sum=el('summary'); if(sum)sum.innerHTML=
      '<div class="summary-item red"><div class="num">'+(sd.red||0)+'</div><div class="lbl">High Priority</div></div>'+
      '<div class="summary-item yellow"><div class="num">'+(sd.yellow||0)+'</div><div class="lbl">Watch</div></div>'+
      '<div class="summary-item gap-item"><div class="num" id="gap-total">--</div><div class="lbl">Knowledge Gaps</div></div>';

    var cards='';
    sigs.slice(0,12).forEach(function(s){
      var c=s.signal.toLowerCase();
      cards+='<div class="signal-card '+c+'" style="border-left:4px solid '+
        (c==='red'?'#ff4d6d':c==='yellow'?'#ffc107':'#18a999')+'">'+
        '<div class="signal-header"><span class="signal-name">'+s.technology+'</span>'+
        '<span class="signal-badge badge-'+c+'">'+s.signal+'</span></div>'+
        '<div class="signal-detail">Heat:'+s.heat_score+' Maturity:'+s.maturity_score+
        ' Commercialization:'+s.commercialization_score+'<br>Score:<b>'+s.composite_score+
        '</b>/10 &middot; '+s.degree+' conn</div>'+
        '<div class="score-bar"><div class="score-fill '+(s.composite_score>7?'high':s.composite_score>4.5?'med':'low')+
        '" style="width:'+Math.round(s.composite_score*10)+'%"></div></div>'+
        ((s.related_companies||[]).length? '<div class="company-tags">'+s.related_companies.map(function(c){return'<span class="tag">'+c+'</span>'}).join('')+'</div>':'')+
      '</div>';
    });
    var g=el('signal-grid'); if(g)g.innerHTML=cards;

    var ch=el('heatmap-chart');
    if(ch){
      var chart=echarts.init(ch);
      var names=sigs.slice(0,15).map(function(s){return s.technology});
      chart.setOption({
        title:{text:'Investment Score Breakdown',textStyle:{fontSize:14}},tooltip:{trigger:'axis'},
        legend:{data:['Heat','Maturity','Commercialization'],textStyle:{color:'#1b2430'}},
        xAxis:{type:'category',data:names,axisLabel:{rotate:30,fontSize:11}},yAxis:{type:'value',max:10},
        series:[
          {name:'Heat',type:'bar',stack:'total',data:sigs.slice(0,15).map(function(s){return s.heat_score}),itemStyle:{color:'#ff4d6d'}},
          {name:'Maturity',type:'bar',stack:'total',data:sigs.slice(0,15).map(function(s){return s.maturity_score}),itemStyle:{color:'#ffc107'}},
          {name:'Commercialization',type:'bar',stack:'total',data:sigs.slice(0,15).map(function(s){return s.commercialization_score}),itemStyle:{color:'#18a999'}}
        ],grid:{left:50,right:20,top:50,bottom:80}});
      window.addEventListener('resize',function(){chart.resize();});
    }

    try{
      var gr=await fetch('/api/gaps');var gd=await gr.json();
      var gt=el('gap-total');if(gt)gt.textContent=gd.total_gaps||0;
      var gh='';
      (gd.gaps||[]).slice(0,10).forEach(function(g){
        var tl=g.type==='missed_synergy'?'Synergy Gap':g.type==='underexplored'?'Underexplored':'Unlinked Eq';
        var tc=g.type==='missed_synergy'?'gap-synergy':g.type==='underexplored'?'gap-underexplored':'gap-equipment';
        gh+='<div class="gap-card"><h4>'+(g.tech_a?g.tech_a+' <-> '+g.tech_b:(g.tech||g.equipment||'?'))+
          '<span class="gap-type '+tc+'">'+tl+'</span></h4><p>'+(g.summary||g.description||'')+'</p></div>';
      });
      var gl=el('gap-list');if(gl)gl.innerHTML=gh;
      var ga=el('gap-analysis');if(ga)ga.innerHTML='<h3>AI Investment Analysis</h3>'+(gd.analysis||'No analysis.').replace(/\\n/g,'<br>');
    }catch(e){console.warn('Gaps:',e);}
  }catch(e){var g=el('signal-grid');if(g)g.innerHTML='<p class="muted">Load failed. Please login and refresh.</p>';}
})();</script>'''
}

# ============================== SIMULATE ==============================
pages['simulate.html'] = {
    'marker': 'simulatePageLoaded',
    'js': '''<script src="/static/js/auth.js"></script>
  <script>
function runPreset(s){document.getElementById('scenario').value=s;runSimulation();}
async function runSimulation(){
  var s=document.getElementById('scenario').value.trim();
  if(!s){alert('Please enter a scenario');return;}
  var b=document.getElementById('run-btn');b.textContent='Running...';b.disabled=true;
  try{
    var r=await fetch('/api/simulate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({scenario:s})});
    var d=await r.json();
    if(d.code==='UNAUTHORIZED'){window.location.href='/login';return;}
    if(d.error){alert(d.error);return;}
    document.getElementById('m-total').textContent=d.affected_count||0;
    document.getElementById('m-paths').textContent=(d.impact_paths||[]).length;
    document.getElementById('m-equip').textContent=(d.equipment_impact||[]).length;
    document.getElementById('m-mat').textContent=(d.material_impact||[]).length;
    document.getElementById('analysis').innerHTML='<h3>AI Impact Analysis</h3>'+(d.analysis||'No analysis.').replace(/\\n/g,'<br>');
    var tags='';(d.affected_nodes||[]).slice(0,15).forEach(function(n){tags+='<span class="shock-tag">'+n+'</span> '});
    document.getElementById('affected-tags').innerHTML=tags?'<div class="tag-list">'+tags+'</div>':'';
    document.getElementById('result').classList.add('show');
  }catch(e){alert('Failed: '+e.message);}
  finally{b.textContent='Simulate\\nImpact';b.disabled=false;}
}
document.getElementById('run-btn').addEventListener('click',runSimulation);
document.getElementById('scenario').addEventListener('keydown',function(e){if(e.key==='Enter'&&e.shiftKey){e.preventDefault();runSimulation();}});
</script>'''
}

# ============================== LEADERBOARD ==============================
pages['leaderboard.html'] = {
    'marker': 'loadLeaderboard',
    'js': '''<script src="/static/js/auth.js"></script>
  <script>
(async function(){
  function el(id){return document.getElementById(id);}
  try{var mr=await fetch('/api/auth/me');var md=await mr.json();
    var ie=el('invite-link');if(ie)ie.value=window.location.origin+'/register?ref='+(md.user?md.user.id:'?');}catch(e){}
  try{
    var r=await fetch('/api/leaderboard');var d=await r.json();var lb=d.leaderboard||[];
    if(d.my_rank){var p=el('my-position');if(p)p.innerHTML='<div class="my-position">Your rank: <b>#'+d.my_rank+'</b> &middot; Reputation: <b>'+(d.my_score||0)+'</b> &middot; Credits: <b>'+(d.my_credits||0)+'</b></div>';}
    var rows='';
    lb.forEach(function(u){
      var rc=u.rank===1?'rank-1':u.rank===2?'rank-2':u.rank===3?'rank-3':'rank-n';
      rows+='<tr><td><span class="rank-badge '+rc+'">'+u.rank+'</span></td>'+
        '<td><div class="user-cell"><div class="user-avatar">'+(u.username?u.username[0].toUpperCase():'?')+'</div>'+
        '<div class="user-info"><div class="user-name">'+u.username+(u.is_verified_pro?' <span class="verified-star">&star;</span>':'')+'</div>'+
        '<div class="user-org">'+(u.company||'')+(u.company&&u.role?' / ':'')+(u.role||'')+'</div></div></div></td>'+
        '<td><b>'+u.reputation_score+'</b><div class="score-bar"><div class="score-fill" style="width:'+Math.round(u.reputation_score)+'%"></div></div></td>'+
        '<td>'+u.contributions_count+'</td><td>'+u.verifications_received+'</td><td>'+(u.badges&&u.badges.length?u.badges.map(function(b){return'<span class="badge-tag '+(b.level==='gold'?'gold':'silver')+'">'+b.name+'</span>'}).join(''):'<span class="muted">--</span>')+'</td></tr>';
    });
    var bd=el('lb-body');if(bd)bd.innerHTML=rows;
  }catch(e){var bd=el('lb-body');if(bd)bd.innerHTML='<tr><td colspan="6" class="muted" style="text-align:center;padding:40px">Failed to load. Please refresh.</td></tr>';}
})();</script>'''
}

# ============================== PROFILE ==============================
pages['profile.html'] = {
    'marker': 'loadProfile',
    'js': '''<script src="/static/js/auth.js"></script>
  <script>
(async function(){
  function el(id){return document.getElementById(id);}
  try{
    var r=await fetch('/api/profile');if(!r.ok)throw new Error('HTTP '+r.status);
    var d=await r.json();
    if(d.code==='UNAUTHORIZED'){window.location.href='/login';return;}
    var u=d.user||{},c=d.credits||{};
    var av=el('pf-avatar');if(av)av.textContent=u.username?u.username[0].toUpperCase():'?';
    var nm=el('pf-name');if(nm)nm.textContent=u.username||'--';
    var og=el('pf-org');if(og)og.textContent=(c.company||'Add your company')+(c.role?' / '+c.role:'');
    var ec=el('edit-company');if(ec)ec.value=c.company||'';
    var er=el('edit-role');if(er)er.value=c.role||'';
    var me=el('pf-metrics');if(me)me.innerHTML=
      '<div class="pf-card"><div class="val">#'+(d.rank||'--')+'</div><div class="lbl">Rank</div></div>'+
      '<div class="pf-card"><div class="val">'+(c.reputation_score||0)+'</div><div class="lbl">Reputation</div></div>'+
      '<div class="pf-card"><div class="val">'+(c.total_credits||0)+'</div><div class="lbl">Credits</div></div>'+
      '<div class="pf-card"><div class="val">'+(c.verifications_received||0)+'</div><div class="lbl">Verifications</div></div>';
    var cs=d.recent_contributions||[],ct='',types={entity_added:'Added Entity',relation_added:'Added Relation',verified_by_peer:'Verified by Peer',referral:'Referral'};
    if(cs.length===0)ct='<p class="muted">No contributions yet.</p>';
    else cs.forEach(function(ci){ct+='<div class="contrib-item"><div><span class="type">'+(types[ci.type]||ci.type)+'</span>'+(ci.entity_name?' &mdash; '+ci.entity_name:'')+'</div><div><span class="credits">+'+ci.credits_earned+'</span></div></div>';});
    var cl=el('contrib-list');if(cl)cl.innerHTML=ct;
  }catch(e){var nm=el('pf-name');if(nm)nm.textContent='Load failed - please refresh';}
})();

async function saveProfile(){
  var c=document.getElementById('edit-company').value.trim();
  var r=document.getElementById('edit-role').value.trim();
  await fetch('/api/profile/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({company:c,role:r})});
  alert('Profile updated!');location.reload();
}
</script>'''
}

# ========== APPLY FIXES ==========
for filename, page in pages.items():
    filepath = os.path.join(TEMPLATES, filename)
    if not os.path.exists(filepath):
        print(f"MISSING: {filename}")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and replace the entire <script> block in the page
    # Strategy: find the last <script> tag before </body> and replace its content
    body_pos = content.rfind('</body>')
    if body_pos == -1:
        body_pos = content.rfind('</html>')
    if body_pos == -1:
        print(f"SKIP {filename}: no </body> found")
        continue

    # Find the last <script> opening before </body>
    script_start = content.rfind('<script>', 0, body_pos)
    if script_start == -1:
        script_start = content.rfind('<script ', 0, body_pos)
    if script_start == -1:
        print(f"SKIP {filename}: no <script> found before </body>")
        continue

    # Find matching </script>
    script_end = content.find('</script>', script_start)
    if script_end == -1:
        print(f"SKIP {filename}: no </script> found")
        continue

    # Replace the JS block
    new_content = content[:script_start] + page['js'] + '\n' + content[script_end + len('</script>'):]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Fixed: {filename}")

print("\nAll pages updated with robust JS.")
