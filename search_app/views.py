from django.shortcuts import render, get_object_or_404, redirect 
from .models import Product,POSITION
from .forms import ProductForm, SearchForm 
from django.core.paginator import Paginator

posi_disc = {}
for ke,va in POSITION:
    posi_disc[va] = ke

def product_create(request): 
    if request.method == 'POST': 
        form = ProductForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            return redirect('product_list') 
    else: 
        form = ProductForm() 
    return render(request, 'product_form.html', {'form': form})

def product_detail(request, pk): 
    product = get_object_or_404(Product, pk=pk) 
    return render(request, 'product_detail.html', {'product': product})

def product_update(request, pk): 
    product = get_object_or_404(Product, pk=pk) 
    if request.method == 'POST': 
        form = ProductForm(request.POST, instance=product) 
        if form.is_valid(): 
            form.save() 
            return redirect('product_detail', pk=product.pk) 
    else: 
        form = ProductForm(instance=product)
    # product オブジェクトをテンプレートに渡す
    return  render(request,'product_form.html',{'form':form,'product':product})

def product_delete(request, pk): 
    product = get_object_or_404(Product, pk=pk) 
    if request.method == 'POST': 
        product.delete() 
        return redirect('product_list') 
    return render(request, 'product_confirm_delete.html', {'product': product})

def product_list(request): 
    products = Product.objects.all() 
    return render(request, 'product_list.html', {'products': products})

def search_view(request): 
    form = SearchForm(request.GET or None)  # フォームのインスタンス化 
    results = Product.objects.all()
    if form.is_valid(): 
        # クリーンデータからクエリ取得 
        query = form.cleaned_data['query']
        if query:
        # 部分一致検索 
            results = results.filter(name__icontains=query) #ここでのfilerはクエリセットに適用
        
    # 身長のフィルタリング（最低身長・最高身長） 
    min_height = request.GET.get('min_height') 
    max_height = request.GET.get('max_height') 
    if min_height: 
        results = results.filter(height__gte=min_height) 
    if max_height: 
        results = results.filter(height__lte=max_height)
        
    # 体重のフィルタリング（最低体重・最大体重） 
    min_weight = request.GET.get('min_weight') 
    max_weight = request.GET.get('max_weight') 
    if min_weight: 
        results = results.filter(weight__gte=min_weight) 
    if max_weight: 
        results = results.filter(weight__lte=max_weight)
    
    #ポジションのフィルタリング
    posi = request.GET.get('position')
    if posi:
        results = results.filter(position=posi_disc[posi])

    # 並び替え処理 
    sort_by = request.GET.get('sort', 'name') 
    if sort_by == 'height_asc': 
        results = results.order_by('height') 
    elif sort_by == 'height_desc': 
        results = results.order_by('-height')
    elif sort_by == 'weight_asc': 
        results = results.order_by('weight')
    elif sort_by == 'weight_desc': 
        results = results.order_by('-weight')
        
    # 1ページに表示する件数を指定（例: 10件ずつ） 
    paginator = Paginator(results, 10)
    # 現在のページ番号をGETリクエストから取得 
    page_number = request.GET.get('page')
    # 指定されたページの結果を取得 
    page_obj = paginator.get_page(page_number)
    
    # テンプレートに結果とページ情報を渡す 
    return render(request, 'search.html', {'form':form,'page_obj': page_obj,'results': results})
