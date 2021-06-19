from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import Post, Comments
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

def index(request):
    template = 'index.html'
    post = Post.objects.all()
    paginator = Paginator(post,3)

    page = request.GET.get('page')
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)

    except EmptyPage:
        post = paginator.page(paginator.num_pages)

    context = {
        'page_obt':page,
        'posts': post}

    return render(request, template_name=template,context=context)


def single_post(request,number,title):
    template = 'single_post.html'
    post = get_object_or_404(Post,slug = title, id = number)
    comment = post.comment_here.filter(active=True) # we got post from the up line and comment_here is taken from related_name of Comments model's post object
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {
        'post':post,
        'comments':comment,
        'new_comment':new_comment,
        'comment_form':comment_form,
    }
    return render(request,template_name=template,context=context)




def post_share(request,post_id):

    post = get_object_or_404(Post,id= post_id,status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.Post)
        if form.is_valid():
            cd = form.cleaned_data
            # .... send email....
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']}  recommends you read" f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject,message,'naeemislam13790@gmail.com', [cd['to']])
            sent = True


    else:
        form = EmailPostForm()
    context = {
        'post':post,
        'form':form,
        'sent':sent
    }
    return render(request,'test.html', context=context)


def test(request):

    test = "hello this a test nothing more bro"

    context = {
       'test': test,
    }
    return render(request,'hi.html',context=context)